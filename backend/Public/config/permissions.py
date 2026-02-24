from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user' and request.user.is_authenticated
    
class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'seller' and request.user.is_authenticated
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' and request.user.is_authenticated


class IsSellerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'seller' or request.user.role == 'admin') and request.user.is_authenticated