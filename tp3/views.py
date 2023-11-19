from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.conf import settings

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

def start_2fa(subject, message, receipient):
    print('before')
    
    print('after')

@api_view(['POST'])
def two_factor_authentication(request):
    subject = ''
    message = ''
    to = ''
    send_mail(
        subject=subject,
        message=message,
        from_email='settings.EMAIL_HOST_USER',
        recipient_list=[to],
        fail_silently=False
    )
    return Response(status=200, data={'done'})