from django.urls import reverse
from django.contrib.auth.models import User
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

    def test_user_create(self):
        """Test that users can be created
        """
        response = self.client.post(reverse('user-list'), data={"username": "test_user", "password": "ASdsa123",
                                                                "email": "test_user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the created user has not superuser rights
        user = User.objects.get_by_natural_key(username='test_user')
        self.assertFalse(user.is_superuser)

    def test_user_create_weak_password(self):
        """Test that password check is working properly
        """
        # Common pattern
        response = self.client.post(reverse('user-list'), data={"username": "test_user", "password": "asdf123",
                                                                "email": "test_user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Too short
        response = self.client.post(reverse('user-list'), data={"username": "test_user", "password": "q#kf",
                                                                "email": "test_user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Only numbers
        response = self.client.post(reverse('user-list'), data={"username": "test_user", "password": "123142141",
                                                                "email": "test_user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_existing_email_or_username(self):
        # Existing email
        response = self.client.post(reverse('user-list'), data={"username": "test_user", "password": "ASdsa123",
                                                                "email": "user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Existing username
        response = self.client.post(reverse('user-list'), data={"username": "user", "password": "ASdsa123",
                                                                "email": "test_user@example.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_update_or_partial_update_admin(self):
        self.authenticate('admin')

        # On update username and email should be different
        response = self.client.put(reverse('user-detail', kwargs={'pk': 1}),
                                   data={"username": "admin1", "password": "ASdsa123", "email": "admin1@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(reverse('user-detail', kwargs={'pk': 1}), data={"password": "ASdsa123dsada"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(reverse('user-detail', kwargs={'pk': 1}), data={"username": "admin"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(reverse('user-detail', kwargs={'pk': 1}), data={"email": "admin@example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
