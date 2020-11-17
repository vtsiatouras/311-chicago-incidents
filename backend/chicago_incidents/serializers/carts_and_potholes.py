"""Carts and potholes related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import NumberOfCartsAndPotholes


class CartsAndPotholesSerializer(ModelSerializer):
    """Carts and potholes create serializer
    """

    class Meta:
        model = NumberOfCartsAndPotholes
        fields = ['number_of_elements']


class CartsAndPotholesSerializerForIncident(CartsAndPotholesSerializer):
    """Carts and potholes create serializer that is used when creating incidents
    """

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
