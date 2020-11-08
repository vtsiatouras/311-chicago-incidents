from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class BaseAPITestCase(APITestCase):
    """Base class for API test cases
    """
    def authenticate(self, username: str):
        """Authenticate the user with the specified email.

        :param username: The username.
        """
        token = RefreshToken.for_user(User.objects.get_by_natural_key(username))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
