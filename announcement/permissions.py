from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only staff users to create, update, or delete announcements.
    Regular users can only read.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, or OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only staff users can create, update, or delete announcements
        return request.user.is_authenticated and request.user.is_staff

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the creator of an announcement or comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access to any user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the creator can modify or delete the object
        return obj.creator == request.user

class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a comment to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only the comment owner can edit or delete the comment
        return obj.user == request.user
