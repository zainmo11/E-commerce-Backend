from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.has_perm("store.add_product")
            )
        )
