"""Views related to authentication
"""
import typing

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg import utils
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework.serializers import Serializer

from .. import serializers


@method_decorator(name='create', decorator=utils.swagger_auto_schema(
    operation_summary="Create user"
))
@method_decorator(name='retrieve', decorator=utils.swagger_auto_schema(
    operation_summary="Get the user details"
))
@method_decorator(name='update', decorator=utils.swagger_auto_schema(
    operation_summary="Update a user"
))
@method_decorator(name='partial_update', decorator=utils.swagger_auto_schema(
    operation_summary="Partial update for a user"
))
class UserProfileViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.RetrieveModelMixin,
                         viewsets.mixins.ListModelMixin, viewsets.mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """User view set
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = User.objects.all()

    def get_queryset(self) -> QuerySet:
        """Return the query set

        :return: The query set
        """
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_serializer_class(self) -> typing.Type[Serializer]:
        """Get the serializer for the action.

        :return: The serializer.
        """
        if self.action in ('retrieve', 'list'):
            return serializers.UserProfileSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.UserCreateProfileSerializer

    def get_permissions(self) -> typing.List[BasePermission]:
        """Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('update', 'partial_update', 'retrieve', 'list'):
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
