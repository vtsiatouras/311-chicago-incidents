"""Sanitation code violation related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import SanitationCodeViolation


class SanitationCodeViolationSerializer(ModelSerializer):
    """Sanitation code violation serializer
    """

    class Meta:
        model = SanitationCodeViolation
        fields = ['id', 'nature_of_code_violation']


class SanitationCodeViolationCreateSerializer(ModelSerializer):
    """Sanitation code violation create serializer
    """

    class Meta:
        model = SanitationCodeViolation
        fields = ['nature_of_code_violation']


class SanitationCodeViolationCreateSerializerForIncident(ModelSerializer):
    """Sanitation code violation create serializer for incident
    """

    class Meta:
        model = SanitationCodeViolation
        fields = ['nature_of_code_violation']
        extra_kwargs = {
            'nature_of_code_violation': {
                'validators': [],
            }
        }
