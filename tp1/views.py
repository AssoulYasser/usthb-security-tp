from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .encryptions import ENCRYPTION_TYPES
from .serializers import *
from .steganography import hide_text, show_text


tempo_path = 'tp1/tempo/'

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
    image_path = tempo_path + 'encrypted_image.png'
    serializer = SteganographyEncryptionSerializer(data=request.data)
    if serializer.is_valid():
        text = request.data['text']
        image = request.data['image']
        hide_text(img_path=image, text=text).save(image_path)

        with open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file, content_type='image/*')
            response['Content-Disposition'] = 'attachment; filename=image.png'
            return response
        
    return Response(status=400)

@api_view(['GET'])
def image_steganography_decryption(request):
    serializer = SteganographyDecryptionSerializer(data=request.data)
    if serializer.is_valid():
        image = request.data['image']
        return Response(status=200, data={"message": show_text(image)})
    