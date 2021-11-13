from rest_framework import permissions
from django_otp import user_has_device
from .utils import otp_is_verified

class IsOtpVerified(permissions.BasePermission):
    """
    If user has verified TOTP device, require TOTP OTP.
    """
    message = "You do not have permission to perform this action until you verify your OTP device."    
    def has_permission(self, request, view):
        if user_has_device(request.user):
            return otp_is_verified(request)
        else:
            return True

class IsOwner(permissions.BasePermission):
    """
    Users can only edit their profiles!
    """
    message = "You can edit only your profile!"    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
