from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .encryptions import *
from .password import *
from .serializers import *
from .steganography import hide_text, show_text


tempo_path = 'tp1/tempo/'

@api_view(['POST'])
def rotation_decryption(request):
    data = request.data
    serializer = RotationDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=left_rotation(data['message']) if data['direction'] == 'right' else left_rotation(data['message'])
        )
    
    return Response(status=400, data=serializer.errors)
    
@api_view(['POST'])
def caesar_decryption(request):
    data = request.data
    serializer = CaesarDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=left_caesar(data['message'], data['caesar_value']) if data['direction'] == 'right' else right_caesar(data['message'], data['caesar_value'])
        )
    
    return Response(status=400, data=serializer.errors)

@api_view(['POST'])
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
        
    return Response(status=400, data=serializer.errors)

@api_view(['POST'])
def image_steganography_decryption(request):
    serializer = SteganographyDecryptionSerializer(data=request.data)
    if serializer.is_valid():
        image = request.data['image']
        return Response(status=200, data={"message": show_text(image)})
    return Response(status=400, data=serializer.errors)
    
@api_view(['POST'])
def password_attack(request):
    data = request.data
    serializer = PasswordAttackSerializer(data=data)

    if serializer.is_valid():
        password = data['password']
        if is_case_1(password):
            return Response(status=200, data=dict_password_1_case(password=password))
        elif is_case_2(password):
            return Response(status=200, data=dict_password_2_case(password=password))
        elif is_case_3(password):
            return Response(status=200, data=force_brut_password_3_case(password=password))
        else:
            return Response(status=400, data={'error': "your password doesn't match any type"})
    return Response(status=400, data=serializer.errors)