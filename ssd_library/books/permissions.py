from rest_framework import permissions


class AreRentedBook(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return str(request.user) in obj.user_rented


