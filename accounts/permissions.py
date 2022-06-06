from rest_framework.permissions import BasePermission
from accounts.utils import is_admin, is_manager, is_student


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        has_perm = is_admin(request.user)
        return has_perm


class IsManager(BasePermission):
    def has_permission(self, request, view):
        has_perm = is_manager(request.user) or is_admin(request.user)
        return has_perm


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        has_perm = is_student(request.user)
        return has_perm
