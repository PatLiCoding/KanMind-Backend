from rest_framework.response import Response
from auth_app.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from boards_app.api.permissions import IsBoardOwnerOrMember
from boards_app.models import Board
from .serializers import BoardSerializer, BoardDetailSerializer, \
    BoardMemberUpdateSerializer, UserMinimalSerializer


class BoardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        boards = Board.objects.filter(
            Q(owner=request.user) |
            Q(members=request.user)
        ).distinct()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)

    def patch(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)
        serializer = BoardMemberUpdateSerializer(
            board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request, board)
        board.delete()
        return Response(status=204)


class EmailCheckView(APIView):
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
        })
