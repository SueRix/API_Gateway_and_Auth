import datetime

import jwt
from django.contrib.auth import get_user_model
from rest_framework import serializers

from base import settings
from .models import CustomUser
from .utils import generate_access_token


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=40)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    user_id = None

    def validate(self, data):
        refresh_token = data.get('refresh')

        if not refresh_token:
            raise serializers.ValidationError('Refresh token is required')

        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Refresh token expired')
        except jwt.DecodeError:
            raise serializers.ValidationError('Invalid refresh token')

        user_id = payload.get('user_id')
        if not user_id:
            raise serializers.ValidationError('Invalid refresh token')

        self.user_id = payload['user_id']

        exp = payload.get('exp')
        if exp and datetime.datetime.utcfromtimestamp(exp) < datetime.datetime.utcnow():
            raise serializers.ValidationError('Refresh token expired')

        return data

    def get_new_access_token(self):
        if self.user_id is None:
            raise serializers.ValidationError("User ID not found")

        user = get_user_model()
        try:
            user = user.objects.get(id=self.user_id)
        except user.DoesNotExist:
            raise serializers.ValidationError("User not found")

        access_token = generate_access_token(user)
        return access_token
