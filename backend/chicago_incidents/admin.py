from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models

admin.site.site_header = _('Chicago Incidents 311 Admin')
admin.site.site_title = _('Chicago Incidents 311 Admin')


@admin.register(models.Incident)
class IncidentAdmin(admin.ModelAdmin):
    """Admin for incidents
    """
    list_display = ('creation_date', 'status', 'completion_date', 'service_request_number',
                    'type_of_service_request', 'street_address', 'zip_code', 'ssa', 'police_district', 'ward',
                    'latitude', 'longitude')
    search_fields = ('service_request_number',)
    ordering = ('service_request_number',)


@admin.register(models.AbandonedVehicle)
class AbandonedVehicleAdmin(admin.ModelAdmin):
    """Admin for abandoned vehicles
    """
    list_display = ('id', 'license_plate', 'vehicle_make_model', 'vehicle_color')
    search_fields = ('license_plate', 'vehicle_make_model', 'vehicle_color')
    ordering = ('license_plate',)


@admin.register(models.AbandonedVehicleIncident)
class AbandonedVehicleIncidentAdmin(admin.ModelAdmin):
    """Admin abandoned vehicle incident
    """
    list_display = ('id', 'incident_service_request', 'license_plate', 'days_of_report_as_parked')
    raw_id_fields = ('incident', 'abandoned_vehicle')

    def incident_service_request(self, obj):
        return obj.incident.service_request_number

    def license_plate(self, obj):
        return obj.abandoned_vehicle.license_plate


@admin.register(models.NumberOfCartsAndPotholes)
class NumberOfCartsAndPotholesAdmin(admin.ModelAdmin):
    """Admin for number of carts and potholes
    """
    list_display = ('id', 'incident_service_request', 'incident_type', 'number_of_elements')
    raw_id_fields = ('incident',)

    def incident_service_request(self, obj):
        return obj.incident.service_request_number

    def incident_type(self, obj):
        return obj.incident.type_of_service_request


@admin.register(models.Graffiti)
class GraffitiAdmin(admin.ModelAdmin):
    """Admin for graffiti
    """
    list_display = ('id', 'surface', 'location')
    search_fields = ('surface', 'location')
    ordering = ('surface',)


@admin.register(models.GraffitiIncident)
class GraffitiIncidentAdmin(admin.ModelAdmin):
    """Admin for graffiti incident
    """
    list_display = ('id', 'incident_service_request', 'graffiti_surface')
    raw_id_fields = ('incident', 'graffiti')

    def incident_service_request(self, obj):
        return obj.incident.service_request_number

    def graffiti_surface(self, obj):
        return obj.graffiti.surface


@admin.register(models.Tree)
class TreeAdmin(admin.ModelAdmin):
    """Admin for tree
    """
    list_display = ('id', 'location')
    search_fields = ('location',)
    ordering = ('location',)


@admin.register(models.TreeIncident)
class TreeIncidentAdmin(admin.ModelAdmin):
    """Admin for tree incident
    """
    list_display = ('id', 'incident_service_request', 'incident_type', 'tree_location')
    raw_id_fields = ('incident', 'tree')

    def incident_service_request(self, obj):
        return obj.incident.service_request_number

    def incident_type(self, obj):
        return obj.incident.type_of_service_request

    def tree_location(self, obj):
        return obj.tree.location


@admin.register(models.RodentBaitingPremises)
class RodentBaitingPremisesAdmin(admin.ModelAdmin):
    """Admin for rodent baiting premises
    """
    list_display = ('id', 'incident_service_request', 'number_of_premises_baited', 'number_of_premises_w_garbage',
                    'number_of_premises_w_rats')
    raw_id_fields = ('incident',)

    def incident_service_request(self, obj):
        return obj.incident.service_request_number


@admin.register(models.SanitationCodeViolation)
class SanitationCodeViolationAdmin(admin.ModelAdmin):
    """Admin for sanitation code violation
    """
    list_display = ('id', 'nature_of_code_violation')
    search_fields = ('nature_of_code_violation',)
    ordering = ('nature_of_code_violation',)


@admin.register(models.SanitationCodeViolationIncident)
class SanitationCodeViolationIncidentAdmin(admin.ModelAdmin):
    """Admin for sanitation code violation incidents
    """
    list_display = ('id', 'incident_service_request', 'sanitation_code')
    raw_id_fields = ('incident',)

    def incident_service_request(self, obj):
        return obj.incident.service_request_number

    def sanitation_code(self, obj):
        return obj.sanitation_code_violation.nature_of_code_violation
