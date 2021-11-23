from rest_framework import permissions
class IsCampaignOwner(permissions.BasePermission):
    message = "You cannot modify an object that you do not own"
    def has_object_permission(self, request, view, obj):
        return request.user == obj.nomination.user
