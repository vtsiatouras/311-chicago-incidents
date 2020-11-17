"""Incident related serializers
"""
from rest_framework.serializers import ModelSerializer, ValidationError

from .. import models
from ..serializers import BaseSerializer, AbandonedVehicleCreateSerializerForIncident, \
    ActivityCreateSerializerForIncident, RodentBaitingPremisesSerializerForIncident, \
    GraffitiCreateSerializerForIncident, CartsAndPotholesCreateSerializer, \
    SanitationCodeViolationCreateSerializerForIncident, TreeCreateSerializerForIncident


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
    activity = ActivityCreateSerializerForIncident(required=False)
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
    activity = ActivityCreateSerializerForIncident(required=False)
    carts_and_potholes = CartsAndPotholesCreateSerializer(required=False)

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
            carts_and_potholes, _ = models.NumberOfCartsAndPotholes.objects. \
                get_or_create(**carts_and_potholes_data, incident=incident)
        if activity_data:
            activity, _ = models.Activity.objects.get_or_create(**activity_data)
            _ = models.ActivityIncident.objects.get_or_create(activity=activity, incident=incident)
        return incident


class GraffitiIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about graffiti
    """
    incident = IncidentCreateSerializer()
    graffiti = GraffitiCreateSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') == models.Incident.GRAFFITI:
            raise ValidationError("'type_of_service_request' should be set as 'GRAFFITI'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        graffiti_data = validated_data.get('graffiti')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if graffiti_data:
            graffiti, _ = models.Graffiti.objects.get_or_create(**graffiti_data)
            _ = models.GraffitiIncident.objects.get_or_create(graffiti=graffiti, incident=incident)
        return incident


class RodentBaitingIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about rodent baiting
    """
    incident = IncidentCreateSerializer()
    activity = ActivityCreateSerializerForIncident(required=False)
    rodent_baiting_premises = RodentBaitingPremisesSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') == models.Incident.RODENT_BAITING:
            raise ValidationError("'type_of_service_request' should be set as 'RODENT_BAITING'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        activity_data = validated_data.get('activity')
        rodent_baiting_premises_data = validated_data.get('rodent_baiting_premises')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if rodent_baiting_premises_data:
            carts_and_potholes, _ = models.RodentBaitingPremises.objects. \
                get_or_create(**rodent_baiting_premises_data, incident=incident)
        if activity_data:
            activity, _ = models.Activity.objects.get_or_create(**activity_data)
            _ = models.ActivityIncident.objects.get_or_create(activity=activity, incident=incident)
        return incident


class SanitationCodeViolationIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about sanitation code violation
    """
    incident = IncidentCreateSerializer()
    sanitation_code_violation = SanitationCodeViolationCreateSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') == models.Incident.SANITATION_CODE:
            raise ValidationError("'type_of_service_request' should be set as 'SANITATION_CODE'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        sanitation_data = validated_data.get('sanitation_code_violation')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if sanitation_data:
            sanitation_code, _ = models.SanitationCodeViolation.objects.get_or_create(**sanitation_data)
            _ = models.SanitationCodeViolationIncident.objects.get_or_create(sanitation_code_violation=sanitation_code,
                                                                             incident=incident)
        return incident


class TreeIncidentCreateSerializer(BaseSerializer):
    """Serializer for creating incidents about trees
    """
    incident = IncidentCreateSerializer()
    activity = ActivityCreateSerializerForIncident(required=False)
    tree = TreeCreateSerializerForIncident(required=False)

    def validate_incident(self, incident):
        if not incident.get('type_of_service_request') in (models.Incident.TREE_TRIM, models.Incident.TREE_DEBRIS):
            raise ValidationError("'type_of_service_request' should be set as 'TREE_TRIM' or 'TREE_DEBRIS'")
        return incident

    def create(self, validated_data):
        incident_data = validated_data.get('incident')
        activity_data = validated_data.get('activity')
        tree_data = validated_data.get('tree')
        incident, _ = models.Incident.objects.get_or_create(**incident_data)
        if tree_data:
            tree, _ = models.Tree.objects.get_or_create(**tree_data)
            _ = models.TreeIncident.objects.get_or_create(tree=tree, incident=incident)
        if activity_data:
            activity, _ = models.Activity.objects.get_or_create(**activity_data)
            _ = models.ActivityIncident.objects.get_or_create(activity=activity, incident=incident)
        return incident
