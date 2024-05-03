from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            request.method in SAFE_METHODS
            or (user.is_authenticated and user.groups.filter(name="Sellers").exists())
        )


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user.is_authenticated and user.groups.filter(name="Sellers").exists()
        )
