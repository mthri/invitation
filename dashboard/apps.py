from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'
    verbose_name = _('پنل')
