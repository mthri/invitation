from typing import List, Optional
import uuid
from datetime import datetime

from django.db import transaction
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_mysql.models import Model
from django_mysql.models import SetCharField
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError as JsonValidationError

from utils.validators import validate_mobile, validate_draft7, validate_template
from utils.config import THUMBNAIL_DIRECTORY_PATH, TEMPLATE_DIRECTORY_PATH
from utils.json_validation import generate_validator_darft7


User = get_user_model()

class BasicField(Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ایجاد'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('آیا حذف شده است؟'))


class Contact(BasicField):
    class Meta:
        verbose_name = _('مخاطب')
        verbose_name_plural = _('مخاطبین')
        index_together = ['owner', 'phone']


    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name=_('نام'), null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'), null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, 
                              verbose_name=_('مالک'), related_name='contacts', 
                              null=True, db_index=True)
    phone = models.CharField(max_length=11, validators=[validate_mobile], null=True, verbose_name=_('تلفن همراه'))
    communicative_road = models.JSONField(verbose_name=('راه های ارتباطی'), null=True, blank=True)
    tags = SetCharField(base_field=models.IntegerField(), size=10, max_length=(10*3), 
                        verbose_name=_('تگ'), null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def get_by_user(user:User):
        return Contact.objects.filter(owner=user).exclude(is_deleted=True)

    @staticmethod
    def sync(contacts: List['Contact']) -> None:
        '''
        check phone number from available social media is registed
        or not
        '''
        # TODO used `bulk_update` https://docs.djangoproject.com/en/3.2/ref/models/querysets/#bulk-update
        ...

    @staticmethod
    def create_contact(first_name:str, last_name:str, user:User,
                       phone, tags:List, communicative_road:dict) -> 'Contact':

        tags = [int(tag) for tag in tags]
        user_tag = set(Tag.get_by_user(user).values_list('id', flat=True))
        # only user tag can be use
        user_tag = user_tag.intersection(tags)

        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            owner=user,
            phone=phone,
            tags=user_tag,
            communicative_road=communicative_road
        )

        contact.save()
        
        return contact

class Tag(BasicField):
    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب ها')
        unique_together = ["owner", "name"]

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, 
                              verbose_name=_('مالک'), related_name='tags', 
                              null=True, db_index=True)
    name = models.CharField(max_length=20, verbose_name=_('نام'), default=_('ندارد'))
    description = models.CharField(max_length=100, verbose_name=_('توضیح'), null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_by_user(user:User):
        return Tag.objects.filter(owner=user)
       

class Template(BasicField):
    class Meta:
        verbose_name = _('قالب')
        verbose_name_plural = _('قالب ها')

    name = models.CharField(max_length=100, verbose_name=_('نام قالب'))
    description = models.CharField(max_length=250, verbose_name=_('توضیحات'))
    # TODO set default thumbnail
    thumbnail = models.ImageField(null=True, blank=True,
                                  upload_to=THUMBNAIL_DIRECTORY_PATH, verbose_name=_('پیش‌نمایش'))
    schema = models.JSONField(validators=[validate_template], verbose_name=_('ساختار'))
    path = models.FileField(verbose_name=_('فایل قالب'), upload_to=TEMPLATE_DIRECTORY_PATH, default='')

    @staticmethod
    def by_id(template_id:int) -> Optional['Template']:
        return Template.objects.filter(pk=template_id).first()
    
    def __str__(self) -> str:
        return self.name + ' | ' + self.description

    def generate_thumbnail(self):
        raise NotImplemented


class Invitation(BasicField):
    class Meta:
        verbose_name = _('دعوت‌نامه')
        verbose_name_plural = _('دعوت‌نامه ها')

    owner = models.ForeignKey(User, verbose_name=_('ایجاد کننده'), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150, verbose_name=_('عنوان'), default=_('ندارد'))
    send_at = models.DateTimeField(null=True, blank=True, verbose_name=_('ارسال در تاریخ'))
    informations = models.JSONField(validators=[validate_draft7], verbose_name=_('اطلاعات اضافی'))
    template = models.ForeignKey(Template, verbose_name=_('قالب'), on_delete=models.SET_NULL, null=True)

    def __str__(self) -> None:
        return str(self.owner) + ' | ' + self.title

    def save(self, *args, **kwargs):
        # validate information with template schema
        Draft7Validator(generate_validator_darft7(self.template.schema['fields'])).validate(self.informations)
        super().save(*args, **kwargs)

    @property
    def is_scheduler(self) -> bool:
        return bool(self.send_at)

    @property
    def is_information_valid(self) -> bool:
        try:
            Draft7Validator(generate_validator_darft7(self.template.schema['fields'])).validate(self.informations)
            return True
        except JsonValidationError:
            return False


    @staticmethod
    def create_invitation(user:User, template:Template, information:dict, is_schedule:bool, contacts:List = None, 
                          tags:List = None, send_at:datetime = None):
        
        invitation = Invitation(owner=user, template=template, informations=information)

        if is_schedule and send_at:
            invitation.send_at = send_at
        
        if not invitation.is_information_valid:
            raise ValueError('schema error')
        else:
            invitation.save()

        contact_list = []

        if contacts:
            contact_list += list(Contact.objects.filter(id__in=contacts))
        
        if tags:
            user_contact = Contact.get_by_user(user)
            contact_list += list(user_contact.filter(tags__contains=tags))
        
        InvitationCard.create_invitation_card(invitation, contact_list)

class InvitationCard(BasicField):

    class Meta:
        verbose_name = _('کارت دعوت')
        verbose_name_plural = _('کارت های دعوت')
        index_together = ["invitation", "is_sent"]


    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, db_index=True)
    invitation = models.ForeignKey(Invitation, verbose_name=_('دعوت'), blank=False, 
                                   null=True, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(Contact, verbose_name=_('مخاطب'), null=True, 
                                blank=False, on_delete=models.DO_NOTHING)
    is_sent = models.BooleanField(default=False, editable=True, verbose_name=_('ارسال شده'))

    def __str__(self) -> str:
        return f'{self.contact} | {self.invitation}  | ' + ('ارسال شده' if self.is_sent else 'ارسال نشده')


    @staticmethod
    @transaction.atomic
    def create_invitation_card(invitation:Invitation, contacts:List[Contact]) -> None:
        invitation_card_bunch = []
        for contact in contacts:
            invitation_card_bunch.append(InvitationCard(
                invitation=invitation,
                contact=contact
            ))
        
        InvitationCard.objects.bulk_create(invitation_card_bunch, batch_size=100)

