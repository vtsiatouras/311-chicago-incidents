"""Views related to authentication
"""
import typing

from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from drf_yasg import utils
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import BasePermission, IsAuthenticated
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
class UserViewSet(viewsets.mixins.CreateModelMixin, viewsets.mixins.RetrieveModelMixin,
                  viewsets.mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """User view set
    """
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self) -> QuerySet:
        """Return the query set

        :return: The query set
        """
        return super().get_queryset()

    def get_serializer_class(self) -> typing.Type[Serializer]:
        """Get the serializer for the action.

        :return: The serializer.
        """
        if self.action == 'retrieve':
            return serializers.UserSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.UserCreateSerializer

    # def get_permissions(self) -> typing.List[BasePermission]:
    #     """Return the permissions for the action.
    #
    #     :return: An array with the permissions for the action.
    #     """
    #     if self.action in ('update', 'partial_update'):
    #         return [IsAuthenticated()]