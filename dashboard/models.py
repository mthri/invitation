import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import indexes
from django.utils.translation import ugettext_lazy as _

from django_mysql.models import Model
from django_mysql.models import JSONField, SetCharField

class Contact(Model):
    class Meta:
        verbose_name = _('مخاطب')
        verbose_name_plural = _('مخاطبین')


    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50, verbose_name=_('نام'), null=True, blank=True)
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'), null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, 
                              verbose_name=_('مالک'), related_name='contacts', 
                              null=True, db_index=True)
    created_at = models.DateTimeField(auto_now=True, editable=False, verbose_name=_('تاریخ ایجاد'))
    communicative_road = JSONField(verbose_name=('راه های ارتباطی'))
    tags = SetCharField(base_field=models.IntegerField(), size=10, max_length=(10*3), 
                        verbose_name=_('تگ'), null=True, blank=True)
    is_deleted = models.BooleanField(default=False, verbose_name=_('آیا حذف شده است؟'))

