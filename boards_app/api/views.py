from rest_framework.response import Response
from auth_app.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from boards_app.api.permissions import IsBoardOwnerOrMember
from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, \
    BoardMemberUpdateSerializer


class BoardViewSet(ModelViewSet):
    """
    ViewSet for automated CRUD operations on Board instances.

    Enforces authentication and custom ownership/membership permission rules.
    Dynamically adjusts querysets and serializers based on the active API
    action.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        """
        Filters the available boards so users can only view or modify boards
        where they are either the owner or a listed member.

        Returns:
            QuerySet: A deduplicated queryset of accessible Board instances.
        """
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        """
        Determines which serializer class to use based on the current action.

        Returns:
            Serializer: BoardDetailSerializer for 'retrieve' (GET single),
                        BoardMemberUpdateSerializer for updates (PUT/PATCH),
                        otherwise the default BoardSerializer.
        """
        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action in ['partial_update', 'update']:
            return BoardMemberUpdateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        """
        Automatically sets the requesting user as the permanent owner of the
        newly created board.

        Args:
            serializer (Serializer): The bound serializer instance.
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view
        requires.

        Bypasses object-level checks during creation because no board instance
        exists yet.

        Returns:
            list: Instantiated permission objects.
        """
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsBoardOwnerOrMember()]


class EmailCheckView(APIView):
    """
    API endpoint to check user existence and retrieve profile details by email.

    Typically used when looking up users to add them as members to a board.

    Permissions:
        - IsAuthenticated (Requires token authorization)
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handles GET requests to fetch basic user info via a query parameter.

        Expected Query Params:
            ?email=user@example.com

        Returns:
            Response: 200 OK with user details if found, 400 Bad Request if
            email parameter is missing, or 404 Not Found if no user matches
            the email.
        """
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)
        user = get_object_or_404(User, email=email)
        return Response({
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname
        }, status=status.HTTP_200_OK)
