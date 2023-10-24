from rest_framework.decorators import api_view
from rest_framework.response import Response
from .encryptions import ENCRYPTION_TYPES

# Create your views here.

@api_view(['GET'])
def decrypt(request):
    message = request.data['message']
    encryption_type = str(request.data['encryption_type'])
    encryption_value = request.data['encryption_value']

    return Response(
        status=200,
        data={
            "message":ENCRYPTION_TYPES[encryption_type]['decryption'](message, encryption_value)
        }
    )
