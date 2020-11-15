"""Incident activity related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import Activity


class ActivitySerializer(ModelSerializer):
    """Activity serializer
    """

    class Meta:
        model = Activity
        fields = ['id', 'current_activity', 'most_recent_action']


class ActivityCreateSerializer(ModelSerializer):
    """Activity create serializer
    """

    class Meta:
        model = Activity
        fields = ['current_activity', 'most_recent_action']

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
