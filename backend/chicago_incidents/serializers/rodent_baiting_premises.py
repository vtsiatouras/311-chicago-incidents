"""Rodent baiting related serializers
"""
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..models import RodentBaitingPremises


class RodentBaitingPremisesSerializer(ModelSerializer):
    """Rodent baiting premises create serializer
    """

    class Meta:
        model = RodentBaitingPremises
        fields = ['number_of_premises_baited', 'number_of_premises_w_garbage', 'number_of_premises_w_rats']

    def validate(self, attrs):
        if attrs['number_of_premises_baited'] is None and attrs['number_of_premises_w_garbage'] is None \
                and attrs['number_of_premises_w_rats'] is None:
            raise ValidationError("Rodent baiting premises fields are all None")
        return attrs


class RodentBaitingPremisesSerializerForIncident(RodentBaitingPremisesSerializer):
    """Rodent baiting premises create serializer that is used when creating incidents
    """

    def get_unique_together_validators(self):
        """Overriding method to disable unique together checks"""
        return []
