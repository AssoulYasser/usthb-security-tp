from rest_framework import serializers
from .encryptions import ENCRYPTION_TYPES, ENCRYPTION_DIRECTIONS

class DefaultEncryptionSerializer(serializers.Serializer):
    sender = serializers.CharField()
    message = serializers.CharField()
    encryption_type = serializers.ChoiceField(choices=ENCRYPTION_TYPES)
    date = serializers.DateTimeField()

class DefaultDecryptionSerializer(serializers.Serializer):
    message = serializers.CharField()

class RotationEncryptionSerializer(DefaultEncryptionSerializer):
    direction = serializers.ChoiceField(choices=ENCRYPTION_DIRECTIONS)

class RotationDecryptionSerializer(DefaultDecryptionSerializer):
    direction = serializers.ChoiceField(choices=ENCRYPTION_DIRECTIONS)

class CaesarEncryptionSerializer(DefaultEncryptionSerializer):
    direction = serializers.ChoiceField(choices=ENCRYPTION_DIRECTIONS)
    caesar_value = serializers.IntegerField()

class CaesarDecryptionSerializer(DefaultDecryptionSerializer):
    direction = serializers.ChoiceField(choices=ENCRYPTION_DIRECTIONS)
    caesar_value = serializers.IntegerField()

class MirrorDecryptionSerializer(DefaultDecryptionSerializer):
    extra_char = serializers.CharField()

class SteganographyEncryptionSerializer(serializers.Serializer):
    text = serializers.CharField()
    image = serializers.ImageField()

class SteganographyDecryptionSerializer(serializers.Serializer):
    image = serializers.ImageField()

class PasswordAttackSerializer(serializers.Serializer):
    password = serializers.CharField()