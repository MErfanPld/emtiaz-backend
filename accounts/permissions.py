from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsApproved(BasePermission):
    """
    Allows access only to users who are both active and managerially approved.
    This is the primary gate for all protected business endpoints.
    """

    message = 'Your account is not approved or is inactive.'

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and getattr(user, 'is_approved', False)
        )


class IsAdminUser(BasePermission):
    """Admin or superuser (staff with proper group or superuser)."""

    message = 'Administrator privileges required.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated and user.is_active):
            return False
        if user.is_superuser:
            return True
        return user.is_staff and user.groups.filter(name__in=['Admin', 'Super Admin']).exists()


class IsAdminOrManager(BasePermission):
    """Admin, Super Admin or Manager groups."""

    message = 'Manager or administrator privileges required.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated and user.is_active and user.is_approved):
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(
            name__in=['Admin', 'Super Admin', 'Manager']
        ).exists()


class IsSelfOrAdmin(BasePermission):
    """Object-level: owner of the object or admin."""

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or (
            user.is_staff and user.groups.filter(name__in=['Admin', 'Super Admin']).exists()
        ):
            return True
        return obj == user
