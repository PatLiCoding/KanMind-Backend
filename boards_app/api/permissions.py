from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH' or request.method == 'GET':
            return (
                obj.owner == request.user or
                obj.members.filter(id=request.user.id).exists()
            )
        elif request.method == 'DELETE':
            return obj.owner == request.user
