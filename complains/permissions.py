from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'staff':  # Staff can reply
            return True
        return obj.user == request.user  # Owner can view/edit
