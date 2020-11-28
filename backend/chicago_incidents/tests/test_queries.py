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
        self.assertEqual(len(response.data), 4)

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

    def test_most_common_service_per_zipcode_missing_date(self):
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
        self.assertEqual(len(response.data), 4)

        response = self.client.get(reverse('queries-average-completion-time-per-request'),
                                   data={'start_date': '2020-09-01', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

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

    def test_most_common_service_in_bounding_box(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-11-15',
                                         'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type_of_service_request'], 'ALLEY_LIGHTS_OUT')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-15',
                                         'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['type_of_service_request'], 'ABANDONED_VEHICLE')

    def test_most_common_service_in_bounding_box_malformed_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01asd', 'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_in_bounding_box_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '', 'a_latitude': 60.0, 'a_longitude': 50.0, 'b_latitude': 50.0,
                                         'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'a_latitude': 60.0, 'a_longitude': 50.0, 'b_latitude': 50.0,
                                         'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_in_bounding_box_malformed_coordinates(self):
        """Test that coordinates validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': "asd60.0", 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': "asd50.0",
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': "asd50.0", 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': "asd60.0"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_in_bounding_box_missing_coordinates(self):
        """Test that coordinates validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_longitude': 50.0, 'b_latitude': 50.0,
                                         'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'b_latitude': 50.0,
                                         'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_most_common_service_in_bounding_box_wrong_coordinates(self):
        """Test that coordinates validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 40.0, 'a_longitude': 50.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-most-common-service-in-bounding-box'),
                                   data={'date': '2020-08-01', 'a_latitude': 60.0, 'a_longitude': 70.0,
                                         'b_latitude': 50.0, 'b_longitude': 60.0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_5_ssa_per_day(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-09-01', 'end_date': '2020-10-01'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_top_5_ssa_per_day_start_date_greater_than_end_date(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'end_date': '2020-08-01', 'start_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_5_ssa_per_day_malformed_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-08-01', 'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-08-01asd', 'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top_5_ssa_per_day_missing_dates(self):
        """Test that date validation works as it should
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'start_date': '2020-08-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-top-5-ssa-per-day'),
                                   data={'end_date': '2020-12-01asd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-top-5-ssa-per-day'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_license_plates(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-license-plates'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # This car appears in 2 open incidents with different address
        self.assertEqual(response.data[0]['license_plate'], 'ASDF1234')

    def test_second_most_common_color(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-second-most-common-color'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['vehicle_color'], 'black')

    def test_rodent_baiting(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'BAITED',
                                                                            'threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'GARBAGE',
                                                                            'threshold': 7})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'RATS',
                                                                            'threshold': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'BAITED',
                                                                            'threshold': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_rodent_baiting_malformed_type_of_premises(self):
        """Test that type of premises validation works
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'Unknown type',
                                                                            'threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': '',
                                                                            'threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_malformed_threshold(self):
        """Test that threshold validation works
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'BAITED',
                                                                            'threshold': "asd3"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'BAITED',
                                                                            'threshold': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-rodent-baiting'), data={'type_of_premises': 'BAITED'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_police_districts(self):
        """Test that this endpoint gives the expected data we want
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 9,
                                                                              'rodent_baiting_threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 2,
                                                                              'rodent_baiting_threshold': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 99,
                                                                              'rodent_baiting_threshold': 99})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_police_districts_malformed_potholes_threshold(self):
        """Test that threshold validation works
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 'asd9',
                                                                              'rodent_baiting_threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': '',
                                                                              'rodent_baiting_threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-police-districts'), data={'rodent_baiting_threshold': 3})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_police_districts_malformed_rodent_baiting_threshold(self):
        """Test that threshold validation works
        """
        self.authenticate('admin')

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 9,
                                                                              'rodent_baiting_threshold': 'asd3'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 9,
                                                                              'rodent_baiting_threshold': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(reverse('queries-police-districts'), data={'potholes_threshold': 9})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
