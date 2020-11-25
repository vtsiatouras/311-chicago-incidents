import typing

from django.db import connection
from django.db.models import Count, Avg, F, Q, CharField
from django.db.models.functions import Concat
from drf_yasg import utils
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from .. import serializers, pagination
from ..models import Incident, AbandonedVehicle


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
        #
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
    def total_requests_per_day(self, request):
        query_params = serializers.DateAndRequestTypeParams(data=self.request.query_params,
                                                            context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data

        # Raw SQL query (printed out executing print(queryset.query)") (%s: input values):
        #
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

    @utils.swagger_auto_schema(
        operation_summary='Find the most common service request per zipcode for a specific day.',
        operation_description='',
        query_serializer=serializers.DateParam
    )
    @action(
        methods=['get'], detail=False, url_path='mostCommonServicePerZipcode',
        serializer_class=serializers.MostFrequentRequestPerZipCodeSerializer
    )
    def most_common_service_per_zipcode(self, request):
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
            cursor.execute('SELECT DISTINCT ON (incidents.zip_code) incidents.zip_code, \
                            incidents.type_of_service_request, \
                            COUNT(incidents.type_of_service_request) AS number_of_requests \
                            FROM incidents \
                            WHERE incidents.zip_code IS NOT NULL AND incidents.creation_date = %s \
                            GROUP BY incidents.zip_code, incidents.type_of_service_request \
                            ORDER BY incidents.zip_code, number_of_requests DESC', [data.get('date')])

            # Flush out the results to list
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                queryset.append(dict(zip(columns, row)))

        serializer = serializers.MostFrequentRequestPerZipCodeSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the average completion time per service request for a specific date range.',
        operation_description='',
        query_serializer=serializers.DateRangeParams
    )
    @action(
        methods=['get'], detail=False, url_path='averageCompletionTimePerRequest',
        serializer_class=serializers.AverageCompletionTimePerRequestSerializer
    )
    def average_completion_time_per_request(self, request):
        query_params = serializers.DateRangeParams(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data

        # Raw SQL query (printed out executing print(queryset.query)") (%s: input values):
        #
        # SELECT "incidents"."type_of_service_request",
        # AVG(("incidents"."completion_date" - "incidents"."creation_date")) AS "average_completion_time"
        # FROM "incidents"
        # WHERE ("incidents"."completion_date" IS NOT NULL
        # AND "incidents"."creation_date" >= %s
        # AND "incidents"."creation_date" <= %s)
        # GROUP BY "incidents"."type_of_service_request"
        # ORDER BY "incidents"."type_of_service_request" ASC
        queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                           creation_date__lte=data.get('end_date')) \
            .values('type_of_service_request') \
            .annotate(average_completion_time=Avg(F('completion_date') - F('creation_date'))) \
            .order_by('type_of_service_request')
        serializer = serializers.AverageCompletionTimePerRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the most common service request in a specified bounding box '
                          '(as designated by GPS-coordinates) for a specific day.',
        operation_description='',
        query_serializer=serializers.DateParamWCoordinates
    )
    @action(
        methods=['get'], detail=False, url_path='mostCommonServiceInBoundingBox',
        serializer_class=serializers.MostFrequentRequestSerializer
    )
    def most_common_request_in_bounding_box(self, request):  # TODO add tests
        query_params = serializers.DateParamWCoordinates(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data

        #                                       lat
        # point a: top left                 a ------- *
        #                                   |         |  long
        #                                   |         |
        # point b: bottom right             * ------- b
        #
        # Raw SQL query (printed out executing print(queryset.query)") (%s: input values):
        #
        # SELECT "incidents"."type_of_service_request",
        # COUNT("incidents"."type_of_service_request") AS "number_of_requests"
        # FROM "incidents"
        # WHERE ("incidents"."creation_date" = %s AND "incidents"."latitude" >= %s
        # AND "incidents"."latitude" <= %s AND "incidents"."longitude" >= %s
        # AND "incidents"."longitude" <= %s)
        # GROUP BY "incidents"."type_of_service_request"
        # ORDER BY "number_of_requests" DESC
        # LIMIT 1
        queryset = Incident.objects.filter(creation_date=data.get('date'),
                                           latitude__range=[data.get('b_latitude'), data.get('a_latitude')],
                                           longitude__range=[data.get('a_longitude'), data.get('b_longitude')]) \
            .values('type_of_service_request') \
            .annotate(number_of_requests=Count('type_of_service_request')) \
            .order_by('-number_of_requests')[:1]

        serializer = serializers.MostFrequentRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the top-5 Special Service Areas (SSA) with regards to total number of requests per '
                          'day for a specific date range (for service requests types that SSA is available: '
                          'abandoned vehicles, garbage carts, graffiti removal, pot holes reported)',
        operation_description='',
        query_serializer=serializers.DateRangeParams
    )
    @action(
        methods=['get'], detail=False, url_path='top5SSA',
        serializer_class=serializers.RequestsPerSSASerializer
    )
    def top_5_ssa_per_day(self, request):   # TODO add tests
        query_params = serializers.DateRangeParams(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data

        # Raw SQL query (printed out executing print(queryset.query)") (%s: input values):
        #
        # SELECT "incidents"."ssa", COUNT("incidents"."service_request_number") AS "number_of_requests"
        # FROM "incidents"
        # WHERE ("incidents"."creation_date" >= %s AND "incidents"."creation_date" <= %s
        # AND "incidents"."ssa" IS NOT NULL)
        # GROUP BY "incidents"."ssa"
        # ORDER BY "number_of_requests" DESC
        # LIMIT 5
        queryset = Incident.objects.filter(creation_date__gte=data.get('start_date'),
                                           creation_date__lte=data.get('end_date'),
                                           ssa__isnull=False) \
            .values('ssa') \
            .annotate(number_of_requests=Count('service_request_number')) \
            .order_by('-number_of_requests')[:5]
        serializer = serializers.RequestsPerSSASerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the license plates (if any) that have been involved in abandoned vehicle complaints '
                          'more than once.',
        operation_description='',
    )
    @action(
        methods=['get'], detail=False, url_path='licensePlates',
        serializer_class=serializers.LicensePlatesSerializer
    )
    def license_plates(self, request):  # TODO tests!
        queryset = []
        with connection.cursor() as cursor:
            # Some details about the following...
            # In order to avoid duplicate requests we can depend on selecting the requests that have status
            # equal to 'OPEN' and counting distinct addresses
            # (what is the possibility to have an another incident with the same vehicle at the same address)
            cursor.execute('SELECT abandoned_vehicles.license_plate, \
                            COUNT(DISTINCT incidents.street_address) AS number_of_requests \
                            FROM abandoned_vehicles \
                            LEFT OUTER JOIN abandoned_vehicles_incidents \
                            ON (abandoned_vehicles.id = abandoned_vehicles_incidents.abandoned_vehicle_id) \
                            LEFT OUTER JOIN incidents \
                            ON (abandoned_vehicles_incidents.incident_id = incidents.id) \
                            WHERE abandoned_vehicles.license_plate IS NOT NULL \
                            AND incidents.status = \'OPEN\' \
                            GROUP BY abandoned_vehicles.license_plate \
                            HAVING COUNT(DISTINCT incidents.street_address) > 1;')
            # Flush out the results to list
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                queryset.append(dict(zip(columns, row)))

        serializer = serializers.LicensePlatesSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the second most common color of vehicles involved in abandoned vehicle complaints.',
        operation_description='',
    )
    @action(
        methods=['get'], detail=False, url_path='secondMostCommonColor',
        serializer_class=serializers.VehicleColorSerializer
    )
    def second_most_common_color(self, request):  # TODO TESTS!
        # Raw SQL:
        #
        # SELECT "abandoned_vehicles"."vehicle_color", COUNT("abandoned_vehicles"."vehicle_color") AS "color_count"
        # FROM "abandoned_vehicles"
        # WHERE "abandoned_vehicles"."vehicle_color" IS NOT NULL
        # GROUP BY "abandoned_vehicles"."vehicle_color"
        # ORDER BY "color_count" DESC
        # LIMIT 1 OFFSET 1
        queryset = AbandonedVehicle.objects.filter(vehicle_color__isnull=False) \
            .values('vehicle_color') \
            .annotate(color_count=Count('vehicle_color')) \
            .order_by('-color_count')[1:2]
        print(queryset.query)
        serializer = serializers.VehicleColorSerializer(queryset, many=True)
        return Response(serializer.data)

    @utils.swagger_auto_schema(
        operation_summary='Find the rodent baiting requests where the number of premises baited or with garbage or '
                          'with rats (on choice) is less than a specified number.',
        operation_description='',
        query_serializer=serializers.RodentBaitingParams
    )
    @action(
        methods=['get'], detail=False, url_path='rodentBaiting',
        pagination_class=pagination.Pagination,
        serializer_class=serializers.IncidentMinifiedSerializer
    )
    def rodent_baiting(self, request):  # TODO tests!
        query_params = serializers.RodentBaitingParams(data=self.request.query_params, context={'request': request})
        query_params.is_valid(raise_exception=True)
        data = query_params.validated_data
        type_of_premises = data.get('type_of_premises')
        # Raw SQL (without pagination)
        #
        # SELECT "incidents"."id", "incidents"."service_request_number", "incidents"."type_of_service_request",
        # "incidents"."street_address", "incidents"."zip_code", "incidents"."latitude", "incidents"."longitude"
        # FROM "incidents"
        # INNER JOIN "rodent_baiting_premises"
        # ON ("incidents"."id" = "rodent_baiting_premises"."incident_id")
        # WHERE "rodent_baiting_premises"."number_of_premises_baited" < 2

        queryset = Incident.objects.values('id', 'service_request_number', 'type_of_service_request',
                                           'street_address', 'zip_code', 'latitude', 'longitude')
        if type_of_premises == serializers.RodentBaitingParams.BAITED:
            queryset = queryset.filter(rodent_baiting_premises__number_of_premises_baited__lt=data.get('threshold')) \
                .order_by('id')
        elif type_of_premises == serializers.RodentBaitingParams.GARBAGE:
            queryset = queryset.filter(rodent_baiting_premises__number_of_premises_w_garbage__lt=data.get('threshold'))\
                .order_by('id')
        elif type_of_premises == serializers.RodentBaitingParams.RATS:
            queryset = queryset.filter(rodent_baiting_premises__number_of_premises_w_rats__lt=data.get('threshold')) \
                .order_by('id')
        else:
            queryset = []

        # Apply pagination to the query
        page = self.paginate_queryset(self.filter_queryset(queryset=queryset))
        serializer = serializers.IncidentMinifiedSerializer(page, many=True)
        return Response(serializer.data)

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        return [IsAuthenticated()]
