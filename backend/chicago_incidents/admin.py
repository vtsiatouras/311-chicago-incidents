from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('Chicago Incidents 311 Admin')
admin.site.site_title = _('Chicago Incidents 311 Admin')


@admin.register(models.Incident)
class IncidentAdmin(admin.ModelAdmin):
    """Admin for incidents
    """
    list_display = ('creation_date', 'status', 'completion_date', 'service_request_number',
                    'type_of_service_request', 'current_activity', 'most_recent_action', 'street_address',
                    'zip_code')
    search_fields = ('service_request_number',)
    ordering = ('service_request_number',)
