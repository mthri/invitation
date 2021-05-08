from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
    verbose_name = _('احراز هویت')
