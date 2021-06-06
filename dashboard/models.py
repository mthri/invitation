from typing import List
from typing_extensions import Required
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import indexes
from django.http import request
from django.utils.translation import ugettext_lazy as _

from django_mysql.models import Model
from django_mysql.models import JSONField, SetCharField

from utils.validators import validate_mobile


User = get_user_model()

class Contact(Model):
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
    created_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('تاریخ ایجاد'))
    phone = models.CharField(max_length=11, validators=[validate_mobile], verbose_name=_('تلفن همراه'))
    communicative_road = models.JSONField(verbose_name=('راه های ارتباطی'))
    tags = SetCharField(base_field=models.IntegerField(), size=10, max_length=(10*3), 
                        verbose_name=_('تگ'), null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_('آیا حذف شده است؟'))

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


class Tag(Model):
    class Meta:
        verbose_name = _('برچسب')
        verbose_name_plural = _('برچسب ها')
        unique_together = ["owner", "name"]

    created_at = models.DateTimeField(auto_now=True, verbose_name=_('تاریخ ایجاد'))
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
       

class Template(Model):
    name = models.CharField(max_length=100, verbose_name=_('نام قالب'))
    description = models.CharField(max_length=250, verbose_name=_('توضیحات'))
    thumbnail = models.ImageField(verbose_name=_('پیش‌نمایش'))
    schema = models.JSONField(verbose_name=_('ساختار'))
    
    def __str__(self) -> str:
        return self.name + ' | ' + self.description