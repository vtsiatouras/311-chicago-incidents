"""Authentication related serializers
"""
from django.contrib.auth.models import User
from django.core import exceptions
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import password_validation


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
            raise serializers.ValidationError({'email': "email: '{}' is used on other account".format(email)})
        return super(UserCreateProfileSerializer, self).validate(email)

    def validate_password(self, password):
        user = self.context['request'].user
        try:
            # validate the password and catch the exception
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(e.messages)

        return super(UserCreateProfileSerializer, self).validate(password)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
