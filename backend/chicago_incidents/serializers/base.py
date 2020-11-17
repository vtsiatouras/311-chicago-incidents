from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """Base serializer that adds default implementation for the create and update methods that do nothing. Serializers
    that do not need those methods can extend this class.
    """

    def create(self, validated_data):
        """Not implemented
        """
        pass

    def update(self, instance, validated_data):
        """Not implemented
        """
        pass
