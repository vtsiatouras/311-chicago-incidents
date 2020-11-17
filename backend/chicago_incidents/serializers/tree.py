"""Tree related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import Tree


class TreeSerializer(ModelSerializer):
    """Tree serializer
    """

    class Meta:
        model = Tree
        fields = ['id', 'location']


class TreeCreateSerializer(ModelSerializer):
    """Tree create serializer
    """

    class Meta:
        model = Tree
        fields = ['location']


class TreeCreateSerializerForIncident(ModelSerializer):
    """Tree create serializer for incident
    """

    class Meta:
        model = Tree
        fields = ['location']
        extra_kwargs = {
            'location': {
                'validators': [],
            }
        }
