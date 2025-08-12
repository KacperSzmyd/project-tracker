from rest_framework.permissions import BasePermission


class IsProjectMember(BasePermission):
    def has_object_permission(self, request, obj, view):
        return request.user in obj.members.all()
