from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from tasks_app.api.permissions import \
    IsTaskCreatorOrBoardOwnerOrMember, \
    IsCommentOwnerOrBoardOwnerOrBoardMember
from rest_framework.exceptions import PermissionDenied
from tasks_app.models import Task, Comments
from django.db.models import Q
from tasks_app.api.serializers import TaskSerializer, \
    TaskDetailSerializer, CommentSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            Q(board__owner=self.request.user) |
            Q(board__members=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return TaskDetailSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        board = serializer.validated_data.get('board')
        if board:
            is_owner = board.owner == self.request.user
            is_member = board.members.filter(id=self.request.user.id).exists()
            if not (is_owner or is_member):
                raise PermissionDenied(
                    "You must be a member or owner of the board to create a task here."
                )
        serializer.save(create_by=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsAuthenticated(), IsTaskCreatorOrBoardOwnerOrMember()]
        return [IsAuthenticated()]


class CommentViewSet(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "comment_pk"

    def get_queryset(self):
        task_pk = self.kwargs.get("pk")
        return Comments.objects.filter(
            Q(task__board__owner=self.request.user) |
            Q(task__board__members=self.request.user),
            task_id=task_pk
        ).distinct()

    def perform_create(self, serializer):
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        is_owner = task.board.owner == self.request.user
        is_member = task.board.members.filter(id=self.request.user.id).exists()
        if not (is_owner or is_member):
            raise PermissionDenied(
                "You do not have permission for this task.")
        serializer.save(author=self.request.user, task_id=task_id)

    def get_permissions(self):
        if self.action in ['create', 'retrieve', 'destroy']:
            return [
                IsAuthenticated(),
                IsCommentOwnerOrBoardOwnerOrBoardMember()]
        return [IsAuthenticated()]


class AssignedView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(board__owner=request.user) | Q(board__members=request.user),
            assignee=request.user
        ).distinct()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewersView(APIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(
            Q(board__owner=request.user) | Q(board__members=request.user),
            reviewer=request.user
        ).distinct()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
