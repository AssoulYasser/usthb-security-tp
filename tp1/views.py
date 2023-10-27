from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .encryptions import *
from .password import *
from .serializers import *
from .steganography import hide_text, show_text


tempo_path = 'tp1/tempo/'

@api_view(['POST'])
def rotation_decryption_request(request):
    data = request.data
    serializer = RotationDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=left_rotation(data['message']) if data['direction'] == 'right' else left_rotation(data['message'])
        )
    
    return Response(status=400, data=serializer.errors)
    
@api_view(['POST'])
def caesar_decryption_request(request):
    data = request.data
    serializer = CaesarDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=caesar_decrypt(encrypted_text=data['message'], shift=data['caesar_value'], direction=data['direction'])
        )
    
    return Response(status=400, data=serializer.errors)

@api_view(['POST'])
def mirror_decryption_request(request):
    data = request.data
    serializer = MirrorDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=mirror_decrypt_phrase(phrase=serializer.validated_data['message'], extra_char=serializer.validated_data['extra_char'])
        )
    return Response(status=400, data=serializer.errors)

@api_view(['POST'])
def affine_decryption_request(request):
    data = request.data
    serializer = AffineDecryptionSerializer(data=data)
    if serializer.is_valid():
        return Response(
            status=200,
            data=affine_decryption(data['message'], data['a'], data['b'])
        )
    return Response(status=400, data=serializer.errors)

@api_view(['POST'])
def image_steganography_encryption_request(request):
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
def image_steganography_decryption_request(request):
    serializer = SteganographyDecryptionSerializer(data=request.data)
    if serializer.is_valid():
        image = request.data['image']
        return Response(status=200, data={"message": show_text(image)})
    return Response(status=400, data=serializer.errors)
    
@api_view(['POST'])
def password_attack_request(request):
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