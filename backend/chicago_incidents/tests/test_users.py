from django.urls import reverse
from rest_framework import status

from .base import BaseAPITestCase


class UserProfileTests(BaseAPITestCase):

    fixtures = ['users.json']

    def test_unauthorized(self):
        """Test that unauthorized access fails
        """
        response = self.client.get(reverse('user-detail'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
