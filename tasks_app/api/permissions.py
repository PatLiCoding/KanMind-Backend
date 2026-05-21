from rest_framework.permissions import BasePermission


class IsTaskCreatorOrBoardOwnerOrMember(BasePermission):
    """
    Custom permission matrix restricting access to Task objects.

    Rules:
        - GET / PATCH: Allowed if the user is the board owner or an assigned
                        board member.
        - DELETE: Restricted strictly to the original task creator or the root
                    board owner.
    """

    def has_object_permission(self, request, view, obj):
        """
        Evaluates object-level permissions on a specific Task instance.
        """
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
    """
    Custom permission matrix restricting access to Comment objects.

    Rules:
        - GET: Allowed if the user belongs to the parent board (as owner or
                member).
        - DELETE: Strictly locked down to the original author of the comment.
    """

    def has_object_permission(self, request, view, obj):
        """
        Evaluates object-level permissions on a specific Comment instance.
        """
        if request.method == 'GET':
            return (
                obj.task.board.owner == request.user or
                obj.task.board.members.filter(id=request.user.id).exists()
            )
        elif request.method == 'DELETE':
            return obj.author == request.user
