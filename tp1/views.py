from rest_framework.decorators import api_view
from rest_framework.response import Response
from .encryptions import ENCRYPTION_TYPES
from .serializers import *
from .steganography import hide_text, show_text

# Create your views here.

@api_view(['GET'])
def text_decryption(request):
    message = request.data['message']
    encryption_type = str(request.data['encryption_type'])
    encryption_value = request.data['encryption_value']

    return Response(
        status=200,
        data={
            "message":ENCRYPTION_TYPES[encryption_type]['decryption'](message, encryption_value)
        }
    )

@api_view(['GET'])
def image_steganography_encryption(request):
    serializer = SteganographyEncryptionSerializer(data=request.data)
    if serializer.is_valid():
        text = request.data['text']
        image = request.data['image']
        return_value = hide_text(img_path=image, text=text)
        return Response(status=200)
    return Response(status=400)