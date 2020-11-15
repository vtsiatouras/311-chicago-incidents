"""Views related to incidents
"""
import typing

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg import utils
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .. import serializers
from ..models import Incident


@method_decorator(name='retrieve', decorator=utils.swagger_auto_schema(
    operation_summary="Get an incident"
))
# @method_decorator(name='update', decorator=utils.swagger_auto_schema(
#     operation_summary="Update an incident"
# ))
# @method_decorator(name='partial_update', decorator=utils.swagger_auto_schema(
#     operation_summary="Partial update for an incident"
# ))
class IncidentViewSet(viewsets.mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    serializer_class = serializers.IncidentSerializer
    queryset = Incident.objects.all()

    # @utils.swagger_auto_schema(query_serializer=serializers.AbandonedVehicleIncidentCreateSerializer)
    @action(
        methods=['post'], detail=False, url_path='create_abandoned_vehicle_incidents',
        serializer_class=serializers.AbandonedVehicleIncidentCreateSerializer,
    )
    def abandoned_vehicle_incident(self, request):
        """Create, update, patch incidents about abandoned vehicles

        :param request: The HTTP request.
        :return: The response.
        """
        serializer = serializers.AbandonedVehicleIncidentCreateSerializer(data=self.request.data,
                                                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    # def get_serializer_class(self) -> typing.Type[Serializer]:
    #     """Get the serializer for the action.
    #
    #     :return: The serializer.
    #     """
    #     if self.action in ('list', 'retrieve'):
    #         return serializers.IncidentSerializer
    #     elif self.action in ('create', 'partial_update', 'update'):
    #         return serializers.AbandonedVehicleIncidentCreateSerializer
