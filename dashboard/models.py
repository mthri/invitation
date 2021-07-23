from typing import List
import uuid

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

class BasicField:
    created_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('تاریخ ایجاد'))
    is_deleted = models.BooleanField(default=False, verbose_name=_('آیا حذف شده است؟'))


class Contact(BasicField, Model):
    class Meta:
        verbose_name = _('مخاطب')
        verbose_name_plural = _('مخاطبین')
        index_together = ["owner", "phone"]
        unique_together = ["owner", "phone"]


    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name=_('نام'), null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'), null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, 
                              verbose_name=_('مالک'), related_name='contacts', 
                              null=True, db_index=True)
    phone = models.CharField(max_length=11, validators=[validate_mobile], null=True, verbose_name=_('تلفن همراه'))
    communicative_road = models.JSONField(verbose_name=('راه های ارتباطی'))
    tags = SetCharField(base_field=models.IntegerField(), size=10, max_length=(10*3), 
                        verbose_name=_('تگ'), null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def get_by_user(user:User):
        return Contact.objects.filter(owner=user)

    @staticmethod
    def sync(contacts: List['Contact']) -> None:
        '''
        check phone number from available social media is registed
        or not
        '''
        # TODO used `bulk_update` https://docs.djangoproject.com/en/3.2/ref/models/querysets/#bulk-update
        ...


class Tag(BasicField, Model):
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
       

class Template(BasicField, Model):
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
    
    def __str__(self) -> str:
        return self.name + ' | ' + self.description

    def generate_thumbnail(self):
        raise NotImplemented


class Invitation(BasicField, Model):
    class Meta:
        verbose_name = _('دعوت‌نامه')
        verbose_name_plural = _('دعوت‌نامه ها')

    owner = models.ForeignKey(User, verbose_name=_('ایجاد کننده'), on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150, verbose_name=_('عنوان'))
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
            Draft7Validator(self.template.schema).validate(self.informations)
            return True
        except JsonValidationError:
            return False
