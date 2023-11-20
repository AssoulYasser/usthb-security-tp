from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import random
from django.core.cache import cache

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']

    try:
        user = MyUser.objects.get(email=email)
        if check_password(password, user.password):
            return Response(status=200, data={'user' : 'found'})
        else:
            return Response(status=200, data={'user' : 'wrong password'})   
    except Exception as E:
        return Response(status=400, data={'error': str(E)})

@api_view(['POST'])
def email_two_factor_authentication(request):
    data = request.data
    serializer = EmailTwoFactorAuthenticationSerializer(data=data)
    if serializer.is_valid():
        subject = 'no-reply'
        message = str(random.randint(11111, 99999))
        cache.set(data['receiver_email'], message, timeout=90)
        receiver_email = data['receiver_email']
        send_mail(
            subject=subject,
            message=message,
            from_email='settings.EMAIL_HOST_USER',
            recipient_list=[receiver_email],
            fail_silently=False
        )
        return Response(status=200, data={'code':message})
    return Response(status=400, data=serializer.error_messages)

@api_view(['POST'])
def get_cached_data(request):
    if cache.get('key'):
        return Response(status=200, data={'found':str(cache.get('key'))})
    cache.set('key', str(random.randint(11111, 99999)), timeout=90)
    return Response(status=200, data={'found':str(cache.get('key'))})
