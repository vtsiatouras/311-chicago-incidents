"""Carts and potholes related serializers
"""
from rest_framework.serializers import ModelSerializer

from ..models import NumberOfCartsAndPotholes


class CartsAndPotholesCreateSerializer(ModelSerializer):
    """Carts and potholes create serializer
    """

    class Meta:
        model = NumberOfCartsAndPotholes
        fields = ['number_of_elements']
