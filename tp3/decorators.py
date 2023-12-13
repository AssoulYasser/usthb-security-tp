import socket
from rest_framework.response import Response
from django.core.cache import cache
from . import rsa
from enum import Enum

class AuthenticationStep(Enum):
    PUBLIC_KEY = 'PUBLIC_KEY'
    PRIVATE_KEY = 'PRIVATE_KEY'
    PASSWORD = 'PASSWORD'
    TWO_FAC_AUTH = 'TWO_FAC_AUTH'
    FACE_RECOGNITION = 'FACE_RECOGNITION'
    ANDROID_ID = 'ANDROID_ID'

def get_local_ip_addresses():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error as e:
        return str(e)

def ALLOW_ONLY_LOCAL_HOST(func):
    def decorator(request):
        LOCAL_HOST = '127.0.0.1'
        local_address = get_local_ip_addresses()
        request_address = request.META.get("REMOTE_ADDR")
        if request_address == local_address or request_address == LOCAL_HOST:
            return func(request)
        else:
            return Response(status=401)
    return decorator

def request_cache_key(request):
    try:
        email = request.data['email']
        local_email = email.split('@')[0]
        request_address = request.META.get("REMOTE_ADDR")
        return f'{local_email}:{request_address}'
    except:
        return None

def REQUEST_RSA_KEY(func):
    def decorator(request):
        cache_key = request_cache_key(request)
        
        if cache_key is None:
            return Response(status=400)

        private_key, public_key = rsa.generate_rsa_key_pair()

        cache.set(cache_key,
                    {
                        AuthenticationStep.PUBLIC_KEY: public_key,
                        AuthenticationStep.PRIVATE_KEY: private_key,
                    }, 
                    timeout=5 * 60
                )

        return func(request)

    return decorator
