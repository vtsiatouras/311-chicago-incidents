from django.conf.urls import url
from django.urls import re_path, include
from rest_auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from . import views


class OptionalSlashRouter(DefaultRouter):
    """Router to make trailing slashes optional. All URLs work with or without trailing slashes, without redirecting.
    """

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register('users', views.UserProfileViewSet, basename='user')

urlpatterns = [
    re_path(r'^auth/?$', TokenObtainPairView.as_view()),
    re_path(r'^auth/refresh/?$', TokenRefreshView.as_view()),
    # re_path(r'^account/password/reset/?$', PasswordResetView.as_view(), name='password_reset'),
    # re_path(
    #     r'^account/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/?$',
    #     PasswordResetConfirmView.as_view(), name='password_reset_confirm'
    # ),
    # re_path(r'^account/password/change/?$', PasswordChangeView.as_view(), name='password_change'),
    url(r'^', include(router.urls))
]
