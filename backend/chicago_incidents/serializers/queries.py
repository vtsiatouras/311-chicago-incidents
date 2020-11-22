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
                                                      help_text='The type of service to group by')


class TotalRequestsPerTypeSerializer(BaseSerializer):
    """The serializer for the total requests per type
    """
    type_of_service_request = serializers.CharField()
    number_of_requests = serializers.IntegerField()
