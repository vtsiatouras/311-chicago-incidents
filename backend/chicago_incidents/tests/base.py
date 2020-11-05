from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# The test user credentials
USER_CREDENTIALS = {
    User: {'email': 'admin@example.com', 'password': 'admin'},
    User: {'email': 'user@example.com', 'password': 'user'}
}


class BaseAPITestCase(APITestCase):
    """Base class for API test cases
    """
    def authenticate(self, email: str):
        """Authenticate the user with the specified email.

        :param email: The user email.
        """
        token = RefreshToken.for_user(User.objects.get_by_natural_key(email))
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token.access_token))
