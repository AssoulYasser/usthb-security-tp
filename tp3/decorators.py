import socket
from rest_framework.response import Response
from django.core.cache import cache
from . import rsa

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
