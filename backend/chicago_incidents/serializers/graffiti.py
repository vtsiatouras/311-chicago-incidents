"""Graffiti related serializers
"""
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..models import Graffiti


class GraffitiSerializer(ModelSerializer):
    """Graffiti serializer
    """

    class Meta:
        model = Graffiti
        fields = ['id', 'surface', 'location']


class GraffitiCreateSerializer(ModelSerializer):
    """Graffiti create serializer
    """

    class Meta:
        model = Graffiti
        fields = ['surface', 'location']

    def validate(self, attrs):
        if attrs['surface'] is None and attrs['location'] is None:
            raise ValidationError("Graffiti fields are all None")
        return attrs


class GraffitiCreateSerializerForIncident(GraffitiCreateSerializer):
    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
