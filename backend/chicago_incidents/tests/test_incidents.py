from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase
from ..models import Incident, AbandonedVehicle, Activity


class IncidentTests(BaseAPITestCase):
    fixtures = ['incidents.json']

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

    def test_abandoned_vehicle_incident_create(self):
        """Test that user can create abandoned vehicle incidents
        """
        self.authenticate('user')

        data = {
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
        }
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that we can create incident without activity
        data.pop('activity')
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate incident and abandoned vehicle
        incident = Incident.objects.filter(service_request_number='987654-qwe')
        self.assertEqual(len(incident), 1)
        abandoned_vehicle = AbandonedVehicle.objects.filter(license_plate='123RT45')
        self.assertEqual(len(abandoned_vehicle), 1)

        # Check that we can create incident without abandoned vehicle & activity
        data.pop('abandoned_vehicle')
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate incident
        incident = Incident.objects.filter(service_request_number='987654-qwe')
        self.assertEqual(len(incident), 1)

        data.update({'activity': {'current_activity': 'Processing request','most_recent_action': 'Get info'}})
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Make sure that we didn't create duplicate incident and activity
        incident = Incident.objects.filter(service_request_number='987654-qwe')
        self.assertEqual(len(incident), 1)
        activity = Activity.objects.filter(current_activity='Processing request')
        self.assertEqual(len(activity), 1)

    def test_abandoned_vehicle_incident_create_malformed_values(self):
        """Test that user can't input malformed values
        """
        self.authenticate('user')

        data = {
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
        }

        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data['incident']['status'] = 'asdf'
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['incident']['status'] = 'OPEN'

        data['incident']['type_of_service_request'] = 'unknown type'
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['incident']['type_of_service_request'] = 'ABANDONED_VEHICLE'

        data['incident']['type_of_service_request'] = 'TREE_TRIMS'
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['incident']['type_of_service_request'] = 'ABANDONED_VEHICLE'

        data['incident']['creation_date'] = 'this is not a date'
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['incident']['type_of_service_request'] = '2020-11-15T23:11:07.285Z'

        data['incident']['service_request_number'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data['incident']['service_request_number'] = '987654-qwe'

        data['activity']['current_activity'] = None
        data['activity']['most_recent_action'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['abandoned_vehicle']['license_plate'] = None
        data['abandoned_vehicle']['vehicle_make_model'] = None
        data['abandoned_vehicle']['vehicle_color'] = None
        response = self.client.post(reverse('incident-abandoned-vehicle-incident'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
