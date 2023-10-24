from rest_framework import serializers

class SteganographyEncryptionSerializer(serializers.Serializer):
    text = serializers.CharField()
    image = serializers.ImageField()

class SteganographyDecryptionSerializer(serializers.Serializer):
    image = serializers.ImageField()