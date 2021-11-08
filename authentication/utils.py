from django_otp import devices_for_user
from django_otp.models import Device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend

def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device

def otp_is_verified(request):
    """
    Helper to determine if user has verified OTP.
    """
    try:
        payload = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'], signing_key=settings.SECRET_KEY).decode(token=request.headers.get('Authorization').split(' ')[1])
    except:
        return False
    persistent_id = payload.get('otp_device_id', False)    
    if persistent_id:
        device = Device.from_persistent_id(persistent_id)
        if (device is not None) and (device.user_id != request.user.id):
            return False
        else:
            # Valid device in JWT
            return True
    else:
        return False
