"""Authentication related serializers
"""
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework.serializers import ModelSerializer, ValidationError
from django.contrib.auth import password_validation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import BaseSerializer


class UserProfileSerializer(ModelSerializer):
    """User serializer
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCreateProfileSerializer(ModelSerializer):
    """User serializer for create action
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise ValidationError({'email': f"email: '{email}' is used on other account"})
        return super(UserCreateProfileSerializer, self).validate(email)

    def validate_password(self, password):
        user = self.context['request'].user
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            raise ValidationError(e.messages)

        return super(UserCreateProfileSerializer, self).validate(password)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.is_superuser = False  # do not create superusers through the API
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, BaseSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['user_name'] = user.username
        token['user_email'] = user.email
        return token
