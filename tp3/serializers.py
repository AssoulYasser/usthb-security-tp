from .models import *
from rest_framework import serializers

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        
        return MyUser.objects.create_user(**validated_data)

class EmailTwoFactorAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyEmailTwoFactorAuthenticationSerializer(EmailTwoFactorAuthenticationSerializer):
    code = serializers.IntegerField()

class FaceRecognitionFactorSerializer(EmailTwoFactorAuthenticationSerializer):
    image = serializers.ImageField()