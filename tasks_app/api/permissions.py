from rest_framework.permissions import BasePermission


class IsTaskCreatorOrBoardOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'GET']:
            return (
                obj.board.owner == request.user or
                obj.board.members.filter(id=request.user.id).exists()
            )
        elif request.method == 'DELETE':
            return (
                obj.create_by == request.user or
                obj.board.owner == request.user
            )


class IsCommentOwnerOrBoardOwnerOrBoardMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return (
                obj.task.board.owner == request.user or
                obj.task.board.members.filter(id=request.user.id).exists()
            )
        elif request.method == 'DELETE':
            return obj.author == request.user
