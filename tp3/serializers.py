from .models import *
from rest_framework import serializers

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EmailTwoFactorAuthenticationSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField()

class VerifyEmailTwoFactorAuthenticationSerializer(EmailTwoFactorAuthenticationSerializer):
    received_code = serializers.IntegerField()