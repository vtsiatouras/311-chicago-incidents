from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase


class UserProfileTests(BaseAPITestCase):

    fixtures = ['users.json']

    def test_unauthorized(self):
        """Test that unauthorized access fails
        """
        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_detail(self):
        """Test that user cam view his own profile details
        """
        self.authenticate('admin')

        response = self.client.get(reverse('user-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
