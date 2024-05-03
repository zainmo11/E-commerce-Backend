from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCustomerAndAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.user.is_authenticated
                and request.user.has_perm("stats.manage_cartitem")
            )
        )


class IsCorrectCustomer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user.id == obj.customer.user.id
