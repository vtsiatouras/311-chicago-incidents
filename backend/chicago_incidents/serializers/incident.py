"""Incident related serializers
"""
from rest_framework.serializers import ModelSerializer

from .. import models
from ..serializers import BaseSerializer, AbandonedVehicleCreateSerializerForIncident, ActivityCreateSerializer, \
    ValidationError, CartsAndPotholesSerializerForIncident


class IncidentSerializer(ModelSerializer):
    """Incident serializer
    """

    class Meta:
        model = models.Incident
        fields = ['id', 'creation_date', 'completion_date', 'status', 'service_request_number',
                  'type_of_service_request', 'street_address', 'zip_code', 'x_coordinate', 'y_coordinate', 'latitude',
                  'ward', 'longitude', 'police_district', 'community_area', 'ssa', 'census_tracts']


class IncidentCreateSerializer(ModelSerializer):
    """Incident serializer
    """

    class Meta:
        model = models.Incident
        fields = ['id', 'creation_date', 'completion_date', 'status', 'service_request_number',
                  'type_of_service_request', 'street_address', 'zip_code', 'zip_codes', 'x_coordinate', 'y_coordinate',
                  'latitude', 'longitude', 'ward', 'wards', 'historical_wards_03_15', 'police_district',
                  'community_area', 'community_areas', 'ssa', 'census_tracts']


class AbandonedVehicleIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about abandoned vehicles
    """
    incident = IncidentCreateSerializer()
    activity = ActivityCreateSerializer(required=False)
    abandoned_vehicle = AbandonedVehicleCreateSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') == models.Incident.ABANDONED_VEHICLE:
            raise ValidationError("'type_of_service_request' should be set as 'ABANDONED_VEHICLE'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        activity_data = validated_data.get('activity')
        abandoned_vehicle_data = validated_data.get('abandoned_vehicle')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if abandoned_vehicle_data:
            abandoned_vehicle, _ = models.AbandonedVehicle.objects.get_or_create(**abandoned_vehicle_data)
            _ = models.AbandonedVehicleIncident.objects.get_or_create(abandoned_vehicle=abandoned_vehicle,
                                                                      incident=incident)
        if activity_data:
            activity, _ = models.Activity.objects.get_or_create(**activity_data)
            _ = models.ActivityIncident.objects.get_or_create(activity=activity, incident=incident)
        return incident


class CartsAndPotholesIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about potholes or garbage carts
    """
    incident = IncidentCreateSerializer()
    activity = ActivityCreateSerializer(required=False)
    carts_and_potholes = CartsAndPotholesSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') in (models.Incident.GARBAGE_CART, models.Incident.POT_HOLE):
            raise ValidationError("'type_of_service_request' should be set as 'GARBAGE_CART' or 'POT_HOLE'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        activity_data = validated_data.get('activity')
        carts_and_potholes_data = validated_data.get('carts_and_potholes')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if carts_and_potholes_data:
            carts_and_potholes, _ = models.NumberOfCartsAndPotholes.objects.\
                get_or_create(number_of_elements=carts_and_potholes_data['number_of_elements'], incident=incident)
        if activity_data:
            activity, _ = models.Activity.objects.get_or_create(**activity_data)
            _ = models.ActivityIncident.objects.get_or_create(activity=activity, incident=incident)
        return incident
