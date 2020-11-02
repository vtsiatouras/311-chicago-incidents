"""Authentication related serializers
"""
from django.apps import apps
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..serializers.base import BaseSerializer


class UserSerializer(ModelSerializer):
    """User serializer
    """

    class Meta:
        model = User
        fields = ['id', 'username']


class UserCreateSerializer(ModelSerializer):
    """User serializer for create action
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        User.objects.create(user=user)
        return user
