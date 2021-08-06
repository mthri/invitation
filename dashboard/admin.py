import json

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models.fields.json import JSONField
from django.utils.translation import ugettext_lazy as _
from django.forms import widgets

from .models import Contact, Tag, Invitation, Template, InvitationCard

class CustomAdmin(admin.AdminSite):
    site_header = _('سامانه دعوت نامه')

admin_site = CustomAdmin()

class PrettyJSONWidget(widgets.Textarea):

    def __init__(self) -> None:
        super().__init__(attrs={'dir':'ltr'})

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True, ensure_ascii=False)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            return super(PrettyJSONWidget, self).format_value(value)
class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


@admin.register(get_user_model(), site=admin_site)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('last_login', )
    exclude = ('password', )

@admin.register(Contact, site=admin_site)
class ContactAdmin(JsonAdmin):
    readonly_fields = ('is_deleted', )
    raw_id_fields = ('owner',)

@admin.register(Tag, site=admin_site)
class TagAdmin(admin.ModelAdmin):
    raw_id_fields = ('owner',)

@admin.register(Template, site=admin_site)
class TemplateAdmin(JsonAdmin):
    pass

@admin.register(Invitation, site=admin_site)
class InvitationAdmin(JsonAdmin):
    raw_id_fields = ('owner',)


@admin.register(InvitationCard, site=admin_site)
class InvitationCardAdmin(JsonAdmin):
    readonly_fields = ('invitation', 'contact')

