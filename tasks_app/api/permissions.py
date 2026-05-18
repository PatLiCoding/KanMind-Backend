from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            obj.owner == request.user or
            obj.members.filter(id=request.user.id).exists()
        )
    
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
        
class IsBoardOwnerOrMemberInComments(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST']:
            return (
                obj.board.owner == request.user or
                obj.board.members.filter(id=request.user.id).exists()
            )
