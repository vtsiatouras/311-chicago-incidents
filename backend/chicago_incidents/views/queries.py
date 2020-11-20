import typing

from drf_yasg import utils
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response


class QueriesViewSet(viewsets.GenericViewSet):

    @utils.swagger_auto_schema(
        operation_summary='the total requests per type that were created within a specified time range and sort them '
                          'in a descending order',
        operation_description='',
        # query_serializer=serializers.ShareOfVoiceContentQueryParams
    )
    @action(
        methods=['get'], detail=False, url_path='totalRequestsPerType',
        # serializer_class=
    )
    def total_requests_per_type(self):
        return Response()

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        return [IsAuthenticated()]
