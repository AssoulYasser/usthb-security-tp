from rest_framework import serializers

class SteganographyEncryptionSerializer(serializers.Serializer):
    text = serializers.CharField()
    image = serializers.ImageField()