from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """
    Custom permission to control access to Board objects based on ownership
    and membership.

    Rules:
        - GET / PATCH: Allowed for both the board owner and any registered
                        board members.
        - DELETE: Strictly restricted to the board owner.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the requesting user has permission to perform the action on
        a specific Board instance.

        Args:
            request (HttpRequest): The incoming API request object.
            view (APIView): The target view handling the request.
            obj (Board): The specific board instance being accessed.

        Returns:
            bool: True if access is granted, False otherwise.
        """
        if request.method == 'PATCH' or request.method == 'GET':
            return (
                obj.owner == request.user or
                obj.members.filter(id=request.user.id).exists()
            )
        elif request.method == 'DELETE':
            return obj.owner == request.user
