import typing

from django.db import connection
from django.db.models import Count
from drf_yasg import utils
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from .. import serializers
from ..models import Incident


class QueriesViewSet(viewsets.GenericViewSet):
    """The queries view set
    """
    queryset = ''

    @utils.swagger_auto_schema(
        operation_summary='Find the total requests per type that were created within a specified time range and sort '
                          'them in a descending order.',
        operation_description='',
        query_serializer=serializers.DateRangeParams
    )
    @action(
        methods=['get'], detail=False, url_path='totalRequestsPerType',
        serializer_class=serializers.TotalRequestsPerTypeSerializer
    )
    def total_requests_per_type(self, request):
        query_params = serializers.DateRangeParams(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data
        # Raw SQL query (printed out executing print(queryset.query)") (%s: input dates):
        # SELECT "incidents"."type_of_service_request", COUNT("incidents"."type_of_service_request") AS
        #   "number_of_requests" FROM "incidents" WHERE ("incidents"."creation_date" >= %s AND
        #   "incidents"."creation_date" <= %s) GROUP BY "incidents"."type_of_service_request"
        #   ORDER BY "number_of_requests" DESC;
        queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                           creation_date__lte=data.get('end_date')) \
            .values('type_of_service_request') \
            .annotate(number_of_requests=Count('type_of_service_request')) \
            .order_by('-number_of_requests')
        serializer = serializers.TotalRequestsPerTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the total requests per day for a specific request type and time range.',
        operation_description='',
        query_serializer=serializers.DateAndRequestTypeParams
    )
    @action(
        methods=['get'], detail=False, url_path='totalRequestsPerDay',
        serializer_class=serializers.TotalRequestsPerDaySerializer
    )
    def total_requests_per_day(self, request):  # TODO needs tests
        query_params = serializers.DateAndRequestTypeParams(data=self.request.query_params,
                                                            context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data

        # Raw SQL query (printed out executing print(queryset.query)") (%s: input values):
        # SELECT "incidents"."creation_date", COUNT("incidents"."service_request_number") AS "number_of_requests"
        # FROM "incidents" WHERE ("incidents"."creation_date" >= %s AND
        # "incidents"."creation_date" <= %s
        # AND "incidents"."type_of_service_request" = %s)
        # GROUP BY "incidents"."creation_date" ORDER BY "incidents"."creation_date" ASC
        queryset = Incident.objects.filter(type_of_service_request=data.get('type_of_service_request'),
                                           creation_date__gte=data.get('start_date'),
                                           creation_date__lte=data.get('end_date')) \
            .values('creation_date') \
            .annotate(number_of_requests=Count('service_request_number')) \
            .order_by('creation_date')

        serializer = serializers.TotalRequestsPerDaySerializer(queryset, many=True)
        return Response(serializer.data)
        # return Response(queryset)

    @utils.swagger_auto_schema(
        operation_summary='Find the most common service request per zipcode for a specific day.',
        operation_description='',
        query_serializer=serializers.DateParam
    )
    @action(
        methods=['get'], detail=False, url_path='mostCommonServicePerZipcode',
        serializer_class=serializers.MostFrequentRequestPerZipCode
    )
    def most_common_service_per_zipcode(self, request):  # TODO needs tests
        query_params = serializers.DateParam(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data
        # This returns all the counts of all requests
        # queryset = Incident.objects.filter(creation_date=data.get('date'), zip_code__isnull=False) \
        #     .values('zip_code', 'type_of_service_request') \
        #     .annotate(number_of_requests=Count('type_of_service_request')) \
        #     .order_by('zip_code')

        queryset = []
        with connection.cursor() as cursor:
            cursor.execute('select distinct on (incidents.zip_code) incidents.zip_code, \
                            incidents.type_of_service_request, \
                            count(incidents.type_of_service_request) as number_of_requests \
                            from incidents \
                            where incidents.zip_code is not null and incidents.creation_date = %s \
                            group by incidents.zip_code, incidents.type_of_service_request \
                            order by incidents.zip_code, number_of_requests desc', [data.get('date')])

            # Flush out the results to list
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                queryset.append(dict(zip(columns, row)))

        serializer = serializers.MostFrequentRequestPerZipCode(queryset, many=True)
        return Response(serializer.data)

    

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        return [IsAuthenticated()]
