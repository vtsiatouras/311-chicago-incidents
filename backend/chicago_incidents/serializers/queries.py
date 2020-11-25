from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chicago_incidents.models import Incident
from chicago_incidents.serializers import BaseSerializer

# The accepted formats for date input
DATE_INPUT_FORMATS = ['%Y-%m-%d']


class DateRangeParams(BaseSerializer):
    """The serializer for the date range.
    """
    start_date = serializers.DateField(required=True, input_formats=DATE_INPUT_FORMATS,
                                       help_text='The start date for data to include')
    end_date = serializers.DateField(required=True, input_formats=DATE_INPUT_FORMATS,
                                     help_text='The end date for data to include')

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise ValidationError({'start_date, end_date': 'start_date must be before end_date'})
        return data


class DateAndRequestTypeParams(DateRangeParams):
    """The serializer for date range and request type
    """
    type_of_service_request = serializers.ChoiceField(choices=Incident.SERVICE_TYPE_CHOICES,
                                                      help_text='The type of service to group by',
                                                      required=True)


class DateParam(BaseSerializer):
    """The serializer for one date
    """
    date = serializers.DateField(required=True, input_formats=DATE_INPUT_FORMATS,
                                 help_text='The date for data to include')


class DateParamWCoordinates(DateParam):
    """The serializer for one date param and a set of coordinates that specify a bounding box
    """
    a_latitude = serializers.FloatField(required=True, help_text='The latitude for point a')
    a_longitude = serializers.FloatField(required=True, help_text='The longitude for point a')
    b_latitude = serializers.FloatField(required=True, help_text='The latitude for point b')
    b_longitude = serializers.FloatField(required=True, help_text='The longitude for point b')


class RodentBaitingParams(BaseSerializer):
    BAITED = 'BAITED'
    GARBAGE = 'GARBAGE'
    RATS = 'RATS'

    TYPE_CHOICES = [
        (BAITED, 'Premises Baited'),
        (GARBAGE, 'Premises With Garbage'),
        (RATS, 'Premises With Rats'),
    ]
    threshold = serializers.IntegerField(required=True, help_text='The specified number')
    type_of_premises = serializers.ChoiceField(choices=TYPE_CHOICES, help_text='The type of the metric to group by')


class TotalRequestsPerTypeSerializer(BaseSerializer):
    """The serializer for the total requests per type
    """
    type_of_service_request = serializers.CharField()
    number_of_requests = serializers.IntegerField()


class TotalRequestsPerDaySerializer(BaseSerializer):
    """The serializer for the total requests per day
    """
    creation_date = serializers.DateTimeField()
    number_of_requests = serializers.IntegerField()


class MostFrequentRequestSerializer(BaseSerializer):
    """The serializer for the most frequent request
    """
    type_of_service_request = serializers.CharField()
    number_of_requests = serializers.IntegerField()


class RequestsPerSSASerializer(BaseSerializer):
    """The serializer for the most frequent request
    """
    ssa = serializers.CharField()
    number_of_requests = serializers.IntegerField()


class MostFrequentRequestPerZipCodeSerializer(MostFrequentRequestSerializer):
    """The serializer for the most frequent request per zip code
    """
    zip_code = serializers.IntegerField()


class AverageCompletionTimePerRequestSerializer(BaseSerializer):
    """The serializer for average completion time per request
    """
    type_of_service_request = serializers.CharField()
    average_completion_time = serializers.CharField()


class LicensePlatesSerializer(BaseSerializer):
    """The serializer for license plates
    """
    license_plate = serializers.CharField()
    number_of_requests = serializers.IntegerField()


class VehicleColorSerializer(BaseSerializer):
    """The serializer for vehicle color
    """
    vehicle_color = serializers.CharField()
    color_count = serializers.IntegerField()
