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
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get_queryset(self):
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BoardDetailSerializer
        if self.action in ['partial_update', 'update']:
            return BoardMemberUpdateSerializer
        return BoardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsBoardOwnerOrMember()]


class EmailCheckView(APIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)
        user = get_object_or_404(User, email=email)
        return Response({
            "id": user.id,
            "email": user.email,
            "fullname": user.fullname
        }, status=status.HTTP_200_OK)
