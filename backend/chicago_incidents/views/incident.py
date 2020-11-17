"""Views related to incidents
"""
import typing

from django.utils.decorators import method_decorator
from drf_yasg import utils
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .. import serializers
from ..models import Incident


@method_decorator(name='retrieve', decorator=utils.swagger_auto_schema(
    operation_summary="Get an incident"
))
@method_decorator(name='create', decorator=utils.swagger_auto_schema(
    operation_summary="Create an incident"
))
class IncidentViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.IncidentSerializer
    queryset = Incident.objects.all()

    # @utils.swagger_auto_schema(query_serializer=serializers.AbandonedVehicleIncidentCreateSerializer)
    @action(
        methods=['post'], detail=False, url_path='createAbandonedVehicleIncidents',
        serializer_class=serializers.AbandonedVehicleIncidentCreateSerializer,
    )
    def abandoned_vehicle(self, request):
        """Create incident about abandoned vehicles

        :param request: The HTTP request.
        :return: The response.
        """
        serializer = serializers.AbandonedVehicleIncidentCreateSerializer(data=self.request.data,
                                                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['post'], detail=False, url_path='createGarbageCartsAndPotholesIncidents',
        serializer_class=serializers.CartsAndPotholesIncidentCreateSerializer,
    )
    def garbage_carts_and_potholes(self, request):
        """Create incident about garbage carts and potholes

        :param request: The HTTP request.
        :return: The response.
        """
        serializer = serializers.CartsAndPotholesIncidentCreateSerializer(data=self.request.data,
                                                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    @action(
        methods=['post'], detail=False, url_path='createRodentBaitingIncidents',
        serializer_class=serializers.RodentBaitingIncidentCreateSerializer,
    )
    def rodent_baiting(self, request):
        """Create incident about rodent baiting

        :param request: The HTTP request.
        :return: The response.
        """
        serializer = serializers.RodentBaitingIncidentCreateSerializer(data=self.request.data,
                                                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_serializer_class(self) -> typing.Type[Serializer]:
        """Get the serializer for the action.

        :return: The serializer.
        """
        if self.action in ('retrieve',):
            return serializers.IncidentSerializer
        elif self.action in ('create',):
            return serializers.IncidentCreateSerializer
        else:
            return super().get_serializer_class()

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        return [IsAuthenticated()]
