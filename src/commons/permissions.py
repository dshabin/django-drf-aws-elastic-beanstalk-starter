from rest_framework.permissions import BasePermission
from django_project.settings import ALLOWED_API_KEYS
import traceback


class RequestIsPost(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return False

class HasAPIKeyAndRequestIsPost(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            api_key = request.headers.get('X-API-KEY',None)
            if api_key in ALLOWED_API_KEYS:
                return True
        return False


class HasAPIKey(BasePermission):

    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-KEY',None)
        if api_key in ALLOWED_API_KEYS:
            return True
        return False