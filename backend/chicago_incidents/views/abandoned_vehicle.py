"""Views related to incidents
"""
import typing

from django.utils.decorators import method_decorator
from drf_yasg import utils
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.serializers import Serializer

from .. import serializers
from ..models import AbandonedVehicle


@method_decorator(name='list', decorator=utils.swagger_auto_schema(
    operation_summary="Get all abandoned vehicles"
))
@method_decorator(name='retrieve', decorator=utils.swagger_auto_schema(
    operation_summary="Get an abandoned vehicle"
))
@method_decorator(name='create', decorator=utils.swagger_auto_schema(
    operation_summary="Create abandoned vehicle"
))
@method_decorator(name='update', decorator=utils.swagger_auto_schema(
    operation_summary="Update an abandoned vehicle"
))
@method_decorator(name='partial_update', decorator=utils.swagger_auto_schema(
    operation_summary="Partial update for an abandoned vehicle"
))
class AbandonedVehicleViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.mixins.CreateModelMixin,
                              viewsets.mixins.UpdateModelMixin, viewsets.mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = serializers.AbandonedVehicleSerializer
    queryset = AbandonedVehicle.objects.all()

    def get_serializer_class(self) -> typing.Type[Serializer]:
        """Get the serializer for the action.

        :return: The serializer.
        """
        if self.action in ('list', 'retrieve'):
            return serializers.AbandonedVehicleSerializer
        elif self.action in ('create', 'partial_update', 'update'):
            return serializers.AbandonedVehicleCreateSerializer

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        return [IsAuthenticated()]
