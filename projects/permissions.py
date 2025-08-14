from rest_framework.permissions import BasePermission


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all() or request.user.is_staff
