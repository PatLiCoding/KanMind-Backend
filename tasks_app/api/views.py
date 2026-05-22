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
    """
    ViewSet for automated CRUD operations on Task instances.

    Enforces user authentication and applies object-level access rules via
    IsTaskCreatorOrBoardOwnerOrMember during safe or destructive mutations.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Dynamically filters available tasks for the 'list' action to only
        show items
        from boards where the active user is either an owner or
        an approved member.

        Returns:
            QuerySet: Deduplicated task records available to the user.
        """
        if self.action == 'list':
            return Task.objects.filter(
                Q(board__owner=self.request.user) |
                Q(board__members=self.request.user)
            ).distinct()
        return Task.objects.all()

    def get_serializer_class(self):
        """
        Determines the appropriate serializer mapping based on the current
        action lifecycle.

        Returns:
            Serializer: TaskDetailSerializer for focused instance lookups and
            updates, otherwise falls back to TaskSerializer.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return TaskDetailSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        """
        Validates target workspace ownership/membership permissions prior to
        persistence, and stamps the request user as the permanent creator of
        the task.

        Raises:
            PermissionDenied: If the request user lacks proper board clearance.
        """
        board = serializer.validated_data.get('board')
        if board:
            is_owner = board.owner == self.request.user
            is_member = board.members.filter(
                id=self.request.user.id).exists()
            if not (is_owner or is_member):
                raise PermissionDenied(
                    "You must be a member or owner of the board to create a"
                    "task here."
                )
        serializer.save(create_by=self.request.user)

    def get_permissions(self):
        """
        Applies object-level verification guardrails exclusively for mutating
        or safe single-lookup steps.

        Returns:
            list: Instantiated permission objects matching
            operational workflows.
        """
        return [IsAuthenticated(), IsTaskCreatorOrBoardOwnerOrMember()]


class CommentViewSet(ModelViewSet):
    """
    ViewSet for nested comment threads tied directly to individual tasks.

    Manages lookups and mutations under strict parent board
    visibility contexts.
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrBoardOwnerOrBoardMember()]
    lookup_url_kwarg = "comment_pk"

    def get_queryset(self):
        """
        Fetches comments for a specific task after asserting parent board
        access.

        Validates that the requesting user is either the owner or a member of
        the underlying board. This prevents unprivileged users from receiving
        anempty array ([]) on list actions, forcing a 403 Forbidden instead.

        Returns:
            QuerySet: Comment records matching the target task routing
            requirements.

        Raises:
            PermissionDenied: If the user lacks access to the parent board.
        """
        task_pk = self.kwargs.get("pk")
        task = get_object_or_404(Task, id=task_pk)
        is_owner = task.board.owner == self.request.user
        is_member = task.board.members.filter(id=self.request.user.id).exists()
        if not (is_owner or is_member):
            raise PermissionDenied(
                "You do not have permission to view comments for this task.")
        return Comments.objects.filter(task_id=task_pk)

    def perform_create(self, serializer):
        """
        Determines the structural access list needed during lifecycle
        operations.

        Bypasses object-level checks during 'create' since the comment instance
        does not exist yet (handled explicitly in perform_create). Enforces
        both authentication and strict object ownership/membership for all
        other actions (list, retrieve, update, destroy).

        Returns:
            list: Instantiated permission objects.
        """
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        is_owner = task.board.owner == self.request.user
        is_member = task.board.members.filter(id=self.request.user.id).exists()
        if not (is_owner or is_member):
            raise PermissionDenied(
                "You do not have permission for this task.")
        serializer.save(author=self.request.user, task_id=task_id)

    def get_permissions(self):
        """
        Determines the structural access list needed during lifecycle
        operations on comments.
        """
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsCommentOwnerOrBoardOwnerOrBoardMember()]


class AssignedView(APIView):
    """
    API endpoint listing tasks explicitly assigned to the requesting user.

    Filters across all accessible workspaces to compile an active task queue.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Processes GET requests to pull task rows where the active user is
        marked as assignee.
        """
        tasks = Task.objects.filter(
            Q(board__owner=request.user) | Q(board__members=request.user),
            assignee=request.user
        ).distinct()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewersView(APIView):
    """
    API endpoint listing tasks where the requesting user is designated as the
    reviewer.

    Provides visibility over task columns requiring verification signatures.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Processes GET requests to pull task rows where the active user is
        marked as reviewer.
        """
        tasks = Task.objects.filter(
            Q(board__owner=request.user) | Q(board__members=request.user),
            reviewer=request.user
        ).distinct()
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
