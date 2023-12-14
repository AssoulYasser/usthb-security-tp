from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .forms import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import random
from .decorators import *
from deepface import DeepFace
from PIL import Image
import os
from . import rsa
from . import cache_settings

OK_STATUS = 200
BAD_STATUS = 400
UNAUTHORIZED_STATUS = 401
NOT_FOUND_STATUS = 404
TIMEOUT_STATUS = 408
UNPROCESSABLE_CONTENT_STATUS = 422
LOCKED_STATUS = 423
SERVER_ERROR_STATUS = 500

def get_ip_address(request):
    return request.META.get("REMOTE_ADDR")

def register(data):
    serializer = MyUserSerializer(data=data)
    if not serializer.is_valid():
        raise ValueError(serializer.error_message)
    serializer.save()

def block_account(email, ip, status):
    user = MyUser.objects.get(email=email)
    user.is_blocked = True
    cracked_layers = []
    match status:
        case cache_settings.AuthenticationStatus.TWO_FAC_AUTH:
            cracked_layers.append(cache_settings.AuthenticationStatus.PASSWORD)
        case cache_settings.AuthenticationStatus.FACE_RECOGNITION:
            cracked_layers.append(cache_settings.AuthenticationStatus.PASSWORD)
            cracked_layers.append(cache_settings.AuthenticationStatus.TWO_FAC_AUTH)
        case cache_settings.AuthenticationStatus.ANDROID_ID:
            cracked_layers.append(cache_settings.AuthenticationStatus.PASSWORD)
            cracked_layers.append(cache_settings.AuthenticationStatus.TWO_FAC_AUTH)
            cracked_layers.append(cache_settings.AuthenticationStatus.FACE_RECOGNITION)
    email_message = f'An unauthorized access attempt has been detected from the IP address: {ip} targeting your account security.'
    if cracked_layers != []:
        email_message += 'Cracked layers are: \n'
        for layer in cracked_layers:
            email_message += '*' + layer.value + '\n'
    email_message = email_message + ' We kindly request you to reach out to our HR department to facilitate unblocking procedures for your account.\n'

    send_mail(
        subject='YOUR ACCOUNT IS BEING CRACKED',
        message= email_message,
        from_email='settings.EMAIL_HOST_USER',
        recipient_list=[email],
        fail_silently=False
    )
    user.save()

def unblock_user(email):
    user = MyUser.objects.get(email=email)
    user.is_blocked = False
    user.save()

def get_last_accessed_account(email, ip):
    user = MyUser.objects.get(email=email)
    access = UnauthorizedAccessHistory.objects.filter(ip_address = ip, user=user)
    access = access.order_by('-access_date')
    return access.first()

@ALLOW_ONLY_LOCAL_HOST
def users(request):
    all_users = MyUser.objects.all()
    add_user_form = MyUserForm()
    context = {
        'users': all_users,
        'add_user_form': add_user_form,
        'message': None
    }

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            request.method = 'PUT'
            email = request.POST.get('user_email')
            unblock_user(email)
            return render(request, 'tp3/index.html', context)
        
        form_result = MyUserForm(request.POST, request.FILES)
        if form_result.is_valid():
            data = form_result.cleaned_data
            try:
                register(data)
                user = data['email']
                message = {
                    'success': True,
                    'data': f'{user} has been saved successfully'
                }
                context['message'] = message
                return render(request, 'tp3/index.html', context)
            except Exception as e:
                message = {
                    'success': False,
                    'data': f'error occured: {e}'
                }
                context['message'] = message
                render(request, 'tp3/index.html', context)
        else:
            message = {
                    'success': False,
                    'data': f'error occured: {form_result.errors.as_data()}'
            }
            context['message'] = message
            render(request, 'tp3/index.html', context)

    if request.method == 'GET':
        context['message'] = None
        return render(request, 'tp3/index.html', context)

    return render(request, 'tp3/index.html', context)

@api_view(['POST'])
def get_rsa_key(request):
    data = request.data
    serializer = EmailSerializer(data=data)
    if serializer.is_valid():
        email = data['email']
        try:
            user = MyUser.objects.get(email=email)
        except:
            return Response(status=NOT_FOUND_STATUS)
        
        if user.is_blocked:
            return Response(status=LOCKED_STATUS)
        
        ip = get_ip_address(request)
        private_key, public_key = rsa.generate_rsa_key_pair()
        try:
            cache_settings.set_private_key(email, ip, private_key)
        except:
            block_account(email, ip, None)
            return Response(status=LOCKED_STATUS)
        
        new_access = UnauthorizedAccessHistory(user=user, ip_address=ip)
        new_access.save()
        return Response(status=OK_STATUS, data={'public_key': public_key})
    
    return Response(status=BAD_STATUS, data={'error': serializer.error_messages})

@api_view(['POST'])
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except Exception as E:
        return Response(status=BAD_STATUS)
    ip = get_ip_address(request)
    
    private_key = cache_settings.get_private_key(email, ip)
    
    if private_key is None:
        return Response(status=TIMEOUT_STATUS) 


    try:
        user = MyUser.objects.get(email=email)
    except Exception as E:
        return Response(status=NOT_FOUND_STATUS)

    try:
        if user.is_blocked:
            raise Exception('THIS ACCOUNT IS BLOCKED')
        cache_settings.check_status_rep(email, ip, cache_settings.AuthenticationStatus.PASSWORD)
    except:
        block_account(email, ip, cache_settings.AuthenticationStatus.PASSWORD)
        return Response(status=LOCKED_STATUS)
    
    try:
        password = rsa.dectyption(private_key_der_b64=private_key, encrypted_data_b64=password)
    except Exception as E:
        return Response(status=UNPROCESSABLE_CONTENT_STATUS)
    
    if check_password(password, user.password):
        cache_settings.validate_status(email, ip, cache_settings.AuthenticationStatus.PASSWORD)
        last_access = get_last_accessed_account(email, ip)
        last_access.password = True
        last_access.save()
        return Response(status=OK_STATUS)
    else:
        return Response(status=UNAUTHORIZED_STATUS)   

@api_view(['POST'])
def email_two_factor_authentication(request):
    data = request.data
    serializer = EmailSerializer(data=data)
    
    if serializer.is_valid():
        email = data['email']
        ip = get_ip_address(request)
        
        if not cache_settings.check_authentication_status(email, ip, cache_settings.AuthenticationStatus.PASSWORD):
            return Response(status=TIMEOUT_STATUS)
        
        try:
            user = MyUser.objects.get(email=email)
            if user.is_blocked:
                raise Exception('THIS ACCOUNT IS BLOCKED')
            cache_settings.check_status_rep(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH)
        except:
            block_account(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH)
            return Response(status=LOCKED_STATUS)

        subject = 'no-reply'
        message = str(random.randint(11111, 99999))
        cache.set(data['email'], message, timeout=90)
        try:
            mail_result = send_mail(
                subject=subject,
                message=message,
                from_email='settings.EMAIL_HOST_USER',
                recipient_list=[email],
                fail_silently=False
            )
            if mail_result:
                cache_settings.set_2fa_code(email, ip, message)
                return Response(status=OK_STATUS)
            return Response(status=SERVER_ERROR_STATUS)
        except Exception as E:
            return Response(status=SERVER_ERROR_STATUS)
    return Response(status=BAD_STATUS, data=serializer.error_messages)

@api_view(['POST'])
def verify_email_two_factory_authentication(request):
    data = request.data
    serializer = VerifyEmailTwoFactorAuthenticationSerializer(data=data)

    if serializer.is_valid():
        email = data['email']
        ip = get_ip_address(request)

        if not cache_settings.check_authentication_status(email, ip, cache_settings.AuthenticationStatus.PASSWORD):
            return Response(status=TIMEOUT_STATUS)
        
        try:
            user = MyUser.objects.get(email=email)
            if user.is_blocked:
                raise Exception('THIS ACCOUNT IS BLOCKED')
            cache_settings.check_status_rep(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH_CODE, allowed_rep=30)
        except:
            block_account(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH_CODE)
            return Response(status=LOCKED_STATUS)

        code = data['code']
        email = data['email']
        if cache_settings.is_2fa_code_valid(email, ip, code):
            cache_settings.validate_status(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH)
            lastest_access = get_last_accessed_account(email, ip)
            lastest_access.email_2fa = True
            lastest_access.save()
            return Response(status=OK_STATUS)
        return Response(status=UNAUTHORIZED_STATUS)
    return Response(status=BAD_STATUS, data={'error':serializer.error_messages})

def save_tempo_image(image, email):
    save_path = f'tp3/tempo/'
    if not os.path.exists(save_path):
        print('gg')
        os.makedirs(save_path)
    image_format = Image.open(image).format
    image_path = save_path + email.split('@')[0] + f'.{image_format}'
    Image.open(image).save(image_path)
    return image_path

@api_view(['POST'])
def face_recognition_factor(request):
    data = request.data
    serializer = FaceRecognitionFactorSerializer(data=data)    
    
    if serializer.is_valid():
        email = data['email']
        image = data['image']
        ip = get_ip_address(request)

        if not cache_settings.check_authentication_status(email, ip, cache_settings.AuthenticationStatus.TWO_FAC_AUTH):
            return Response(status=TIMEOUT_STATUS)
        
        try:
            user = MyUser.objects.get(email=email)
            if user.is_blocked:
                raise Exception('THIS ACCOUNT IS BLOCKED')
            cache_settings.check_status_rep(email, ip, cache_settings.AuthenticationStatus.FACE_RECOGNITION)
        except:
            block_account(email, ip, cache_settings.AuthenticationStatus.FACE_RECOGNITION)
            return Response(status=LOCKED_STATUS)
        
        user = MyUser.objects.get(email=email)
        user_photo_path = user.personal_image
        path_to_sent_image = save_tempo_image(image=image, email=email)
        try:
            verify = DeepFace.verify(img1_path=str(user_photo_path), img2_path=path_to_sent_image, model_name='VGG-Face')
        except Exception as E:
            return Response(status=UNPROCESSABLE_CONTENT_STATUS)
        if verify['verified']:
            cache_settings.validate_status(email, ip, cache_settings.AuthenticationStatus.FACE_RECOGNITION)
            lastest_access = get_last_accessed_account(email, ip)
            lastest_access.face_id = True
            lastest_access.last_photo = image
            lastest_access.save()
            return Response(status=OK_STATUS)
        return Response(status=UNAUTHORIZED_STATUS)
    return Response(status=BAD_STATUS, data={'error': serializer.error_messages})

@api_view(['POST'])
def android_id(request):
    data = request.data
    serializer = AndroidIdFactorSerializer(data=data)

    if serializer.is_valid():
        email = data['email']
        android_id = request.data['android_id']
        ip = get_ip_address(request)

        if not cache_settings.check_authentication_status(email, ip, cache_settings.AuthenticationStatus.FACE_RECOGNITION):
            return Response(status=TIMEOUT_STATUS)
    
        try:
            user = MyUser.objects.get(email=email)
        except:
            return Response(status=NOT_FOUND_STATUS)
        
        try:
            if user.is_blocked:
                raise Exception('THIS ACCOUNT IS BLOCKED')
            cache_settings.check_status_rep(email, ip, cache_settings.AuthenticationStatus.ANDROID_ID, allowed_rep=1)
        except:
            block_account(email, ip, cache_settings.AuthenticationStatus.ANDROID_ID)
            return Response(status=LOCKED_STATUS)
        
        private_key = cache_settings.get_private_key(email, ip)
    
        if private_key is None:
            return Response(status=TIMEOUT_STATUS)
        
        try:
            android_id = rsa.dectyption(private_key_der_b64=private_key, encrypted_data_b64=android_id)
        except Exception as E:
            return Response(status=UNPROCESSABLE_CONTENT_STATUS)
        
        if user.android_id == android_id:
            last_access = get_last_accessed_account(email, ip)
            last_access.delete()
            AuthorizedAccessHistory(user=user, ip_address=ip).save()
            return Response(status=OK_STATUS)
        return Response(status=UNAUTHORIZED_STATUS)