from rest_framework import permissions
from user.models import User

class IsUserWriteOnly(permissions.BasePermission):
    message = 'User Account must be Your own.'

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj == request.user
        
