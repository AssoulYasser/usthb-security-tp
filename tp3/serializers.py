from .models import *
from rest_framework import serializers

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        field = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

class EmailTwoFactorAuthenticationSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField()