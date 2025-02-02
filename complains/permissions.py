from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    """ Only owner can view/edit, staff can reply """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:  # Staff can reply
            return True
        return obj.user == request.user  # Owner can view/edit
