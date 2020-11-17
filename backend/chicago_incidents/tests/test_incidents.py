from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase
from ..models import AbandonedVehicle, Activity, Graffiti, SanitationCodeViolation


class IncidentTests(BaseAPITestCase):
    fixtures = ['incidents.json']

    def setUp(self) -> None:
        self.__data__ = [
            {'creation_date': '2020-11-15T23:11:07.285Z',
             'completion_date': '2020-11-15T23:11:07.285Z',
             'status': 'OPEN',
             'service_request_number': '987654-qwe',
             'type_of_service_request': 'ABANDONED_VEHICLE',
             'street_address': 'Test Address 123',
             'zip_code': 0,
             'zip_codes': 0,
             'x_coordinate': 12.134,
             'y_coordinate': 12.134,
             'latitude': 12.134,
             'longitude': 12.134,
             'ward': 0,
             'wards': 0,
             'historical_wards_03_15': 0,
             'police_district': 0,
             'community_area': 0,
             'community_areas': 0,
             'ssa': 0,
             'census_tracts': 0
             },
            {
                'incident': {
                    'creation_date': '2020-11-15T23:11:07.285Z',
                    'completion_date': '2020-11-15T23:11:07.285Z',
                    'status': 'OPEN',
                    'service_request_number': '987654-qwe',
                    'type_of_service_request': 'ABANDONED_VEHICLE',
                    'street_address': 'Test Address 123',
                    'zip_code': 0,
                    'zip_codes': 0,
                    'x_coordinate': 12.134,
                    'y_coordinate': 12.134,
                    'latitude': 12.134,
                    'longitude': 12.134,
                    'ward': 0,
                    'wards': 0,
                    'historical_wards_03_15': 0,
                    'police_district': 0,
                    'community_area': 0,
                    'community_areas': 0,
                    'ssa': 0,
                    'census_tracts': 0
                },
                'activity': {
                    'current_activity': 'Processing request',
                    'most_recent_action': 'Get info'
                },
                'abandoned_vehicle': {
                    'license_plate': '123RT45',
                    'vehicle_make_model': 'Test Model',
                    'vehicle_color': 'Red'
                }
            },
            {
                'incident': {
                    'creation_date': '2020-11-15T23:11:07.285Z',
                    'completion_date': '2020-11-15T23:11:07.285Z',
                    'status': 'OPEN',
                    'service_request_number': '987654-qwe',
                    'type_of_service_request': 'POT_HOLE',
                    'street_address': 'Test Address 123',
                    'zip_code': 0,
                    'zip_codes': 0,
                    'x_coordinate': 12.134,
                    'y_coordinate': 12.134,
                    'latitude': 12.134,
                    'longitude': 12.134,
                    'ward': 0,
                    'wards': 0,
                    'historical_wards_03_15': 0,
                    'police_district': 0,
                    'community_area': 0,
                    'community_areas': 0,
                    'ssa': 0,
                    'census_tracts': 0
                },
                'activity': {
                    'current_activity': 'Processing request',
                    'most_recent_action': 'Get info'
                },
                'carts_and_potholes': {
                    'number_of_elements': '100',
                }
            },
            {
                'incident': {
                    'creation_date': '2020-11-15T23:11:07.285Z',
                    'completion_date': '2020-11-15T23:11:07.285Z',
                    'status': 'OPEN',
                    'service_request_number': '987654-qwe',
                    'type_of_service_request': 'RODENT_BAITING',
                    'street_address': 'Test Address 123',
                    'zip_code': 0,
                    'zip_codes': 0,
                    'x_coordinate': 12.134,
                    'y_coordinate': 12.134,
                    'latitude': 12.134,
                    'longitude': 12.134,
                    'ward': 0,
                    'wards': 0,
                    'historical_wards_03_15': 0,
                    'police_district': 0,
                    'community_area': 0,
                    'community_areas': 0,
                    'ssa': 0,
                    'census_tracts': 0
                },
                'activity': {
                    'current_activity': 'Processing request',
                    'most_recent_action': 'Get info'
                },
                'rodent_baiting_premises': {
                    'number_of_premises_baited': 10,
                    'number_of_premises_w_garbage': 30,
                    'number_of_premises_w_rats': 20
                }
            },
            {
                'incident': {
                    'creation_date': '2020-11-15T23:11:07.285Z',
                    'completion_date': '2020-11-15T23:11:07.285Z',
                    'status': 'OPEN',
                    'service_request_number': '987654-qwe',
                    'type_of_service_request': 'GRAFFITI',
                    'street_address': 'Test Address 123',
                    'zip_code': 0,
                    'zip_codes': 0,
                    'x_coordinate': 12.134,
                    'y_coordinate': 12.134,
                    'latitude': 12.134,
                    'longitude': 12.134,
                    'ward': 0,
                    'wards': 0,
                    'historical_wards_03_15': 0,
                    'police_district': 0,
                    'community_area': 0,
                    'community_areas': 0,
                    'ssa': 0,
                    'census_tracts': 0
                },
                'graffiti': {
                    'surface': 'test surface',
                    'location': 'test location',
                }
            },
            {
                'incident': {
                    'creation_date': '2020-11-15T23:11:07.285Z',
                    'completion_date': '2020-11-15T23:11:07.285Z',
                    'status': 'OPEN',
                    'service_request_number': '987654-qwe',
                    'type_of_service_request': 'SANITATION_CODE',
                    'street_address': 'Test Address 123',
                    'zip_code': 0,
                    'zip_codes': 0,
                    'x_coordinate': 12.134,
                    'y_coordinate': 12.134,
                    'latitude': 12.134,
                    'longitude': 12.134,
                    'ward': 0,
                    'wards': 0,
                    'historical_wards_03_15': 0,
                    'police_district': 0,
                    'community_area': 0,
                    'community_areas': 0,
                    'ssa': 0,
                    'census_tracts': 0
                },
                'sanitation_code_violation': {
                    'nature_of_code_violation': 'test violation',
                }
            }
        ]

    def test_unauthorized(self):
        """Test that unauthorized access fails
        """
        response = self.client.get(reverse('incident-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_incident_detail(self):
        """Test that user cam view a specific incident
        """
        self.authenticate('user')

        response = self.client.get(reverse('incident-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_incident_create(self):
        """Test that user can create simple incidents
        """
        self.authenticate('user')

        data = self.__data__[0]

        response = self.client.post(reverse('incident-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_incident_create_twice(self):
        """Test that user can't create the same incident twice or more
        """
        self.authenticate('user')

        data = self.__data__[0]

        response = self.client.post(reverse('incident-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(reverse('incident-list'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[0]

        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incident_create_malformed_service_request(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[0]
        data['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[0]

        data['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incident_create_malformed_service_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[0]
        data['service_request_number'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create(self):
        """Test that user can create abandoned vehicle incidents
        """
        self.authenticate('user')

        data = self.__data__[1]

        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_abandoned_vehicle_incident_create_twice(self):
        """Test that user can't create same abandoned vehicle incidents twice or more
        """
        self.authenticate('user')

        data = self.__data__[1]

        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that we can't create the same incident twice
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_w_o_activity(self):
        """Test that user can create abandoned vehicle incidents without activity
        """
        self.authenticate('user')

        data = self.__data__[1]
        data.pop('activity')
        data['incident']['service_request_number'] = 'srn1'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_abandoned_vehicle_incident_create_w_o_abandoned_vehicle(self):
        """Test that user can create abandoned vehicle incidents without abandoned vehicle
        """
        self.authenticate('user')

        data = self.__data__[1]
        data.pop('abandoned_vehicle')
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_abandoned_vehicle_incident_create_w_o_activity_and_abandoned_vehicle(self):
        """Test that user can create abandoned vehicle incidents without activity and abandoned vehicle
        """
        self.authenticate('user')

        data = self.__data__[1]
        data.pop('activity')
        data.pop('abandoned_vehicle')
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_abandoned_vehicle_incident_create_does_not_creating_duplicate_activities_and_abandoned_cars(self):
        """Test that creating incidents with same activities do not create duplicate activities and cars to the db
        """
        self.authenticate('user')

        data = self.__data__[1]
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['incident']['service_request_number'] = 'srn3'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate activity
        activity = Activity.objects.filter(current_activity='Processing request')
        abandoned_car = AbandonedVehicle.objects.filter(license_plate='123RT45')
        self.assertEqual(len(activity), 1)
        self.assertEqual(len(abandoned_car), 1)

    def test_abandoned_vehicle_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_malformed_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_wrong_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_malformed_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_malformed_activity(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['activity']['current_activity'] = None
        data['activity']['most_recent_action'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_abandoned_vehicle_incident_create_malformed_abandoned_vehicle(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[1]

        data['abandoned_vehicle']['license_plate'] = None
        data['abandoned_vehicle']['vehicle_make_model'] = None
        data['abandoned_vehicle']['vehicle_color'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create(self):
        """Test that user can create garbage carts and potholes incidents
        """
        self.authenticate('user')

        data = self.__data__[2]
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check for 'GARBAGE_CART' as type of request
        data['incident']['type_of_service_request'] = 'GARBAGE_CART'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_potholes_and_carts_incident_create_twice(self):
        """Test that user can't create the same incident twice
        """
        self.authenticate('user')

        data = self.__data__[2]
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_w_o_activity(self):
        """Test that user can create incident without activity
        """
        self.authenticate('user')

        data = self.__data__[2]
        data.pop('activity')
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_potholes_and_carts_incident_create_w_o_carts_and_potholes(self):
        """Test that user can create incident without carts-and-potholes
        """
        self.authenticate('user')

        data = self.__data__[2]
        data.pop('carts_and_potholes')
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_potholes_and_carts_incident_create_w_o_carts_and_potholes_and_activity(self):
        """Test that user can create incident without carts-and-potholes & activity
        """
        self.authenticate('user')

        data = self.__data__[2]
        data.pop('activity')
        data.pop('carts_and_potholes')
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_potholes_and_carts_incident_create_does_not_creating_duplicate_activities(self):
        """Test that creating incidents with same activities do not create duplicate activities to the db
        """
        self.authenticate('user')

        data = self.__data__[2]

        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['incident']['service_request_number'] = 'srn2'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate activity
        activity = Activity.objects.filter(current_activity='Processing request')
        self.assertEqual(len(activity), 1)

    def test_potholes_and_carts_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_malformed_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_wrong_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_malformed_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_malformed_activity(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]
        data['activity']['current_activity'] = None
        data['activity']['most_recent_action'] = None
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_potholes_and_carts_incident_create_malformed_carts_and_potholes(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[2]

        data['carts_and_potholes']['number_of_elements'] = None
        response = self.client.post(reverse('incident-garbage-carts-and-potholes'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create(self):
        """Test that user can create rodent baiting incidents
        """
        self.authenticate('user')

        data = self.__data__[3]
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rodent_baiting_incident_create_twice(self):
        """Test that user can't create rodent baiting incidents twice
        """
        self.authenticate('user')

        data = self.__data__[3]

        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_w_o_activity(self):
        """Test that user can create rodent baiting incidents without activity
        """
        self.authenticate('user')

        data = self.__data__[3]
        data.pop('activity')
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rodent_baiting_incident_create_w_o_rodent_baiting_premises(self):
        """Test that user can create rodent baiting incidents without rodent baiting premises
        """
        self.authenticate('user')

        data = self.__data__[3]

        data.pop('rodent_baiting_premises')
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rodent_baiting_incident_create_w_o_activity_and_rodent_baiting_premises(self):
        """Test that user can create rodent baiting incidents without activity and rodent baiting premises
        """
        self.authenticate('user')

        data = self.__data__[3]
        data.pop('activity')
        data.pop('rodent_baiting_premises')
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rodent_baiting_incident_create_does_not_creating_duplicate_activities(self):
        """Test that creating incidents with same activities do not create duplicate activities to the db
        """
        self.authenticate('user')

        data = self.__data__[3]
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['incident']['service_request_number'] = 'srn2'
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        activity = Activity.objects.filter(current_activity='Processing request')
        self.assertEqual(len(activity), 1)

    def test_rodent_baiting_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_malformed_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_wrong_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_malformed_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_malformed_activity(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['activity']['current_activity'] = None
        data['activity']['most_recent_action'] = None
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rodent_baiting_incident_create_malformed_rodent_baiting(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[3]
        data['rodent_baiting_premises']['number_of_premises_baited'] = None
        data['rodent_baiting_premises']['number_of_premises_w_garbage'] = None
        data['rodent_baiting_premises']['number_of_premises_w_rats'] = None
        response = self.client.post(reverse('incident-rodent-baiting'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create(self):
        """Test that user can create graffiti incidents
        """
        self.authenticate('user')

        data = self.__data__[4]
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_graffiti_incident_create_twice(self):
        """Test that user can't create the same incident twice
        """
        self.authenticate('user')

        data = self.__data__[4]
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_w_o_graffiti(self):
        """Test that user can create incident without graffiti
        """
        self.authenticate('user')

        data = self.__data__[4]
        data.pop('graffiti')
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_graffiti_incident_create_does_not_creating_duplicate_graffiti(self):
        """Test that creating incidents with same activities do not create duplicate graffiti to the db
        """
        self.authenticate('user')

        data = self.__data__[4]

        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['incident']['service_request_number'] = 'srn2'
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate activity
        graffiti = Graffiti.objects.filter(surface='test surface')
        self.assertEqual(len(graffiti), 1)

    def test_graffiti_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]

        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_malformed_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]

        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_wrong_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]

        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]

        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_malformed_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]

        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_graffiti_incident_create_malformed_graffiti(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[4]
        data['graffiti']['surface'] = None
        data['graffiti']['location'] = None
        response = self.client.post(reverse('incident-graffiti'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create(self):
        """Test that user can create sanitation code violation incidents
        """
        self.authenticate('user')

        data = self.__data__[5]
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sanitation_code_violation_incident_create_twice(self):
        """Test that user can't create the same incident twice
        """
        self.authenticate('user')

        data = self.__data__[5]
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_w_o_sanitation_code_violation(self):
        """Test that user can create incident without sanitation code violation
        """
        self.authenticate('user')

        data = self.__data__[5]
        data.pop('sanitation_code_violation')
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sanitation_code_violation_incident_create_does_not_creating_duplicate_sanitation_code_violation(self):
        """Test that creating incidents with same activities do not create duplicate sanitation code violation to the db
        """
        self.authenticate('user')

        data = self.__data__[5]

        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['incident']['service_request_number'] = 'srn2'
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate activity
        code_violation = SanitationCodeViolation.objects.filter(nature_of_code_violation='test violation')
        self.assertEqual(len(code_violation), 1)

    def test_sanitation_code_violation_incident_create_malformed_status(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_malformed_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_wrong_type_of_service(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_malformed_dates(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_malformed_request_number(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sanitation_code_violation_incident_create_sanitation_code_violation(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = self.__data__[5]

        data['sanitation_code_violation']['nature_of_code_violation'] = None
        response = self.client.post(reverse('incident-sanitation-code-violation'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
