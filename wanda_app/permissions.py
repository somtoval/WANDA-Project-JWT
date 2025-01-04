from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    """
    Custom permission to allow only users in the 'admin' group.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the 'admin' group
        return request.user and request.user.groups.filter(name='admin').exists()
