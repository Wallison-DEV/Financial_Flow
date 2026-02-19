from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'account'):
            return obj.account.user == request.user
        if hasattr(obj, 'credit_card'):
            return obj.credit_card.account.user == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return False