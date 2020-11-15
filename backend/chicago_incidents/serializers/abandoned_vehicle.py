"""Abandoned vehicle related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import AbandonedVehicle


class AbandonedVehicleSerializer(ModelSerializer):
    """Abandoned vehicle serializer
    """

    class Meta:
        model = AbandonedVehicle
        fields = ['id', 'license_plate', 'vehicle_make_model', 'vehicle_color']


class AbandonedVehicleCreateSerializer(ModelSerializer):
    """Abandoned vehicle create serializer
    """

    class Meta:
        model = AbandonedVehicle
        fields = ['license_plate', 'vehicle_make_model', 'vehicle_color']


class AbandonedVehicleCreateSerializerForIncident(AbandonedVehicleCreateSerializer):
    """Abandoned vehicle create serializer that is used when creating incidents
    """

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
