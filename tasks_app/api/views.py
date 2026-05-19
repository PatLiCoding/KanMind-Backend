from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from tasks_app.api.permissions import IsBoardOwnerOrMember,\
      IsTaskCreatorOrBoardOwnerOrMember,\
          IsBoardOwnerOrMemberInComments,IsOwnerInComments
from tasks_app.models import Task, Comments
from django.db.models import Q
from tasks_app.api.serializers import TaskSerializer,\
      TaskDetailSerializer, CommentsSerializer,\
          CommentsDetailSerializer


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
        serializer = TaskSerializer(
            data=request.data, context={'request': request})
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
    

class TaskDetailView(APIView):
    permission_classes = [
        IsAuthenticated, IsTaskCreatorOrBoardOwnerOrMember]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        serializer = TaskDetailSerializer(
            task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=204)
    

class AssignedView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(assignee=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ReviewersView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(reviewer=request.user)
        ).distinct()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CommentsView(APIView):
    permission_classes = [
        IsAuthenticated, IsBoardOwnerOrMemberInComments]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        comments = task.comments.all()
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)
        serializer = CommentsSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(
                author=request.user,
                task_id=task_id
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerInComments]

    def get(self, request, task_id, comment_id):
        comment = get_object_or_404(
            Comments, id=comment_id, task_id=task_id)
        self.check_object_permissions(request, comment)
        serializer = CommentsDetailSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, task_id, comment_id):
        comment = get_object_or_404(
            Comments, id=comment_id, task_id=task_id)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=204)


