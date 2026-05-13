from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from boards_app.api.permissions import IsBoardOwnerOrMember
from tasks_app.models import Task
from boards_app.models import Board
from django.db.models import Q
from tasks_app.api.serializers import TaskSerializer


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(board__owner=request.user) |
            Q(board__members=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
