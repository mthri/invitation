from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import ugettext_lazy as _, gettext

from utils.validators import validate_mobile

class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
      if password is None:
          raise TypeError('Superusers must have a password.')

      user = self.create_user(username, email, password)
      user.is_superuser = True
      user.is_staff = True
      user.save()

      return user

class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

    username = models.CharField(db_index=True, max_length=100, unique=True, verbose_name=_('نام کاربری'))
    first_name = models.CharField(max_length=100, null=True, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, null=True, verbose_name=_('نام خانوادگی'))
    email = models.EmailField(db_index=True, unique=True, verbose_name=_('ایمیل'))
    phone = models.CharField(max_length=11, validators=[validate_mobile], unique=True, verbose_name=_('تلفن همراه'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'