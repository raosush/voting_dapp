from datetime import timedelta
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
from .utils import get_user_totp_device

# User Serializer
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User.objects.create(username=validated_data['username'], email=validated_data['email'], password=validated_data['password'])
    return user

class TOTPCustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        device = get_user_totp_device(user)
        if (user is not None) and (device is not None) and (device.user_id == user.id) and (device.confirmed is True):
            token['otp_device_id'] = device.persistent_id
        else:
            token['otp_device_id'] = None
        return token

class TOTPCustomTokenRefreshSerialzier(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        access_token = refresh.access_token
        if access_token.payload.get('otp_device_id', False):
            access_token.set_exp(lifetime=timedelta(hours=settings.CUSTOM_AUTH_VALUES['ACCESS_TOKEN_LIFETIME']))
        data = {'access': str(access_token)}

        if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
            if settings.SIMPLE_JWT['BLACKLIST_AFTER_ROTATION']:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            if access_token.payload.get('otp_device_id', False):
                refresh.set_exp(lifetime=timedelta(hours=settings.CUSTOM_AUTH_VALUES['REFRESH_TOKEN_LIFETIME']))
            else:
                refresh.set_exp()
            refresh.set_iat()

            data['refresh'] = str(refresh)

        return data
