import logging

from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.utils.html import DOTS
from django.utils.translation import ugettext_lazy as _, gettext

from django_mysql.models import EnumField

from utils.validators import validate_mobile

logger = logging.getLogger(__name__)

class User(AbstractUser):
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    class GenderChoices(models.TextChoices):
        MAN = 'M', _('مذکر')
        FEMALE = 'F', _('مونث')
        OTHER = 'O', _('غیره')

    email = models.EmailField(db_index=True, unique=True, verbose_name=_('ایمیل'))
    phone = models.CharField(max_length=11, validators=[validate_mobile], unique=True, verbose_name=_('تلفن همراه'))
    gender = EnumField(choices=GenderChoices.choices,  verbose_name=_('جنسیت'), null=True, blank=True, 
                       default=GenderChoices.OTHER)
    cash = models.IntegerField(null=False, blank=False, editable=True, verbose_name=_('موجودی'), default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @staticmethod
    def get_by_phone(phone):
        return User.objects.filter(phone=phone).first()
    
    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_by_username(username):
        return User.objects.filter(username=username).first()
