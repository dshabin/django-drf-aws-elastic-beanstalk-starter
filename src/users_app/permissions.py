from rest_framework.permissions import BasePermission
from .models import User

class IsUserObjectOwner(BasePermission):
    
    def has_permission(self, request, view):
        try:
            user = User.objects.get(user=request.user,id=view.kwargs['id'])
        except:
            return False
        return True