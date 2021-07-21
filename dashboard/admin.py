from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .models import Contact, Tag, Invitation, Template

class CustomAdmin(admin.AdminSite):
    site_header = _('سامانه دعوت نامه')

admin_site = CustomAdmin()

@admin.register(get_user_model(), site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('last_login', )
    exclude = ('password', )

@admin.register(Contact, site=admin_site)
class ContactAdmin(admin.ModelAdmin):
    readonly_fields = ('is_deleted', )
    #TODO load user lazy

@admin.register(Tag, site=admin_site)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Template, site=admin_site)
class TemplateAdmin(admin.ModelAdmin):
    pass

@admin.register(Invitation, site=admin_site)
class InvitationAdmin(admin.ModelAdmin):
    pass
