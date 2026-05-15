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
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(board__owner=request.user) |
            Q(board__members=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class AssignedView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(assignees=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ReviewersView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(reviewers=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
