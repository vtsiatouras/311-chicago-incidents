from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase
from ..models import Incident


class QueriesTests(BaseAPITestCase):
    fixtures = ['incidents.json']

    def test_unauthorized(self):
        """Test that unauthorized access fails
        """
        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-07-10',
                                                                                     'end_date': '2020-09-10'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_total_requests_per_type(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01',
                                                                                     'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01',
                                                                                     'end_date': '2020-10-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_total_requests_per_type_start_date_greater_than_end_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'end_date': '2020-08-01',
                                                                                     'start_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_type_malformed_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01asd',
                                                                                     'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01',
                                                                                     'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01asd',
                                                                                     'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_type_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'start_date': '2020-08-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_day(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01',
                                         'type_of_service_request': 'ABANDONED_VEHICLE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-10-01',
                                         'type_of_service_request': 'ABANDONED_VEHICLE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_total_requests_per_day_start_date_greater_than_end_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'end_date': '2020-08-01', 'start_date': '2020-12-01',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_day_malformed_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01asd',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01asd',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_day_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01asd', 'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'end_date': '2020-12-01asd', 'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'type_of_service_request': 'ALLEY_LIGHTS_OUT'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_day_malformed_type_of_service_request(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01',
                                         'type_of_service_request': 'ALLEY_LIGHTS_OUTasdf'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01',
                                         'type_of_service_request': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_total_requests_per_day_missing_type_of_service_request(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-total-requests-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_per_zipcode(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-per-zipcode'),
                                   data={'date': '2020-11-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(reverse('queries-most-common-service-per-zipcode'),
                                   data={'date': '2020-08-15'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_most_common_service_per_zipcode_malformed_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-per-zipcode'), data={'date': '2020-08-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_per_zipcode_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-per-zipcode'), data={'date': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-total-requests-per-type'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_average_completion_time_per_request(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-09-01', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_average_completion_time_per_request_start_date_greater_than_end_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'end_date': '2020-08-01', 'start_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_average_completion_time_per_request_malformed_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_average_completion_time_per_request_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-08-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-average-completion-time-per-request'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
