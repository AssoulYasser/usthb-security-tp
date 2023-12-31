from django.core.cache import cache
from enum import Enum

class AuthenticationStatus(Enum):
    PASSWORD = 'PASSWORD'
    TWO_FAC_AUTH = 'TWO_FAC_AUTH'
    TWO_FAC_AUTH_CODE = 'TWO_FAC_AUTH_CODE'
    FACE_RECOGNITION = 'FACE_RECOGNITION'
    ANDROID_ID = 'ANDROID_ID'

AUTHENTICATION_PROCCESS_REPEATED = '_REPEATED'
AUTHENTICATION_PROCCESS_STATUS_REP_DURATION = 24*60*60
ALLOWED_AUTHENTICATION_PROCCESS_REP = 5

AUTHENTICATION_PROCCESS_STATUS_DURATION = 10*60

def request_authentication_cache_key(email, ip):
    try:
        return f'{email}:{ip}'
    except:
        return None

def set_private_key(email, ip, private_key):
    key = request_authentication_cache_key(email, ip)
    cache.set(key, private_key, timeout=AUTHENTICATION_PROCCESS_STATUS_DURATION)
    repetetion_key = key + AUTHENTICATION_PROCCESS_REPEATED
    repeated = cache.get(repetetion_key)
    if repeated is None:
        cache.set(repetetion_key, 1, timeout=AUTHENTICATION_PROCCESS_STATUS_REP_DURATION)
    elif repeated >= ALLOWED_AUTHENTICATION_PROCCESS_REP:
        raise Exception('ACCOUNT SHOULD BE BLOCKED')
    else:
        cache.set(repetetion_key, repeated + 1, timeout=AUTHENTICATION_PROCCESS_STATUS_REP_DURATION)

def get_private_key(email, ip):
    key = request_authentication_cache_key(email, ip)
    return cache.get(key)

def validate_status(email, ip, status):
    key = request_authentication_cache_key(email, ip)
    cache.set(key + status.value, True, timeout= AUTHENTICATION_PROCCESS_STATUS_DURATION)

def check_status_rep(email, ip, status, allowed_rep=ALLOWED_AUTHENTICATION_PROCCESS_REP):
    key = request_authentication_cache_key(email, ip) + status.value + AUTHENTICATION_PROCCESS_REPEATED
    cached_rep = cache.get(key)
    if cached_rep is None:
        cache.set(key, 1, timeout=AUTHENTICATION_PROCCESS_STATUS_DURATION)
    elif cached_rep >= allowed_rep:
        raise Exception('ACCOUNT SHOULD BE BLOCKED')
    else:
        cache.set(key, cached_rep+1, timeout=AUTHENTICATION_PROCCESS_STATUS_DURATION)

def check_authentication_status(email, ip, status):
    key = request_authentication_cache_key(email, ip)

    if cache.get(key) is None:
        return False
    
    ANDROID_ID = cache.get(key + AuthenticationStatus.ANDROID_ID.value)
    FACE_RECOGNITION = cache.get(key + AuthenticationStatus.FACE_RECOGNITION.value)
    TWO_FAC_AUTH = cache.get(key + AuthenticationStatus.TWO_FAC_AUTH.value)
    PASSWORD = cache.get(key + AuthenticationStatus.PASSWORD.value)

    match status:
        case AuthenticationStatus.ANDROID_ID:
            return ANDROID_ID and FACE_RECOGNITION and TWO_FAC_AUTH and PASSWORD
        case AuthenticationStatus.FACE_RECOGNITION:
            return FACE_RECOGNITION and TWO_FAC_AUTH and PASSWORD
        case AuthenticationStatus.TWO_FAC_AUTH:
            return TWO_FAC_AUTH and PASSWORD
        case AuthenticationStatus.PASSWORD:
            return PASSWORD
    
def set_2fa_code(email, ip, code):
    key = request_authentication_cache_key(email, ip) + AuthenticationStatus.TWO_FAC_AUTH_CODE.value
    cache.set(key, code, timeout=90)

def is_2fa_code_valid(email, ip, code):
    key = request_authentication_cache_key(email, ip) + AuthenticationStatus.TWO_FAC_AUTH_CODE.value
    if cache.get(key) == code:
        cache.delete(key)
        return True
    return False
