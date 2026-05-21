from auth_app.models import User
from tasks_app.models import Task, Comments
from boards_app.models import Board
from django.db.models import Q
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


class TaskSerializer(serializers.ModelSerializer):
    """
    Standard serializer for managing tasks.

    Validates that assignees and reviewers belong to the selected board,
    calculates dynamic comments metrics, and tracks who created the task.
    """
    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=False,
        allow_null=True
    )
    comments = serializers.PrimaryKeyRelatedField(
        queryset=Comments.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description',
            'status', 'priority', 'assignee_id',
            'assignee', 'reviewer_id', 'reviewer',
            'due_date', 'comments', 'comments_count',
        ]

    def get_comments_count(self, obj):
        """Computes total count of child comments attached to this task."""
        return obj.comments.count()

    def _validate_board_member(self, user, field_name):
        """
        Internal helper to assert that a target user is either the owner
        or an active group member of the assigned parent board.
        """
        if not user:
            return None
        board_id = self.initial_data.get('board') or (
            self.instance.board.id if self.instance else None)
        is_valid_member = Board.objects.filter(
            Q(id=board_id) & (Q(owner=user) | Q(members=user))
        ).exists()
        if not is_valid_member:
            raise serializers.ValidationError(
                f"The selected {field_name} is not a member of this board.")
        return user

    def validate_assignee_id(self, value):
        """Validates that the task assignee is an authorized board member."""
        return self._validate_board_member(value, "assignee")

    def validate_reviewer_id(self, value):
        """Validates that the task reviewer is an authorized board member."""
        return self._validate_board_member(value, "reviewer")

    def create(self, validated_data):
        """Creates a Task instance, automatically binding the active
        request user as creator."""
        request = self.context.get('request')
        if request:
            validated_data['create_by'] = request.user
        comments = validated_data.pop('comments', [])
        task = Task.objects.create(**validated_data)
        task.create_by = request.user
        task.comments.set(comments)
        return task


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Detailed read-only serializer for individual Task inspection.

    Optimized for view configurations that require nested structural
    user objects instead of shallow entity IDs.
    """
    assignee = UserMinimalSerializer(read_only=True)
    reviewer = UserMinimalSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assignee',
        write_only=True,
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='reviewer',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'assignee',
            'assignee_id',
            'reviewer',
            'reviewer_id',
            'due_date',
        ]

    def _validate_board_member(self, user, field_name):
        """
        Internal validation helper mirroring root TaskSerializer layout rules.
        """
        if not user:
            return user
        board_id = self.initial_data.get('board') or (
            self.instance.board.id if self.instance else None)
        is_valid_member = Board.objects.filter(
            Q(id=board_id) & (Q(owner=user) | Q(members=user))
        ).exists()
        if not is_valid_member:
            raise serializers.ValidationError(
                f"The selected {field_name} is not a member of this board.")
        return user

    def validate_assignee_id(self, value):
        """Asserts validity of assigned member during updates."""
        return self._validate_board_member(value, "assignee")

    def validate_reviewer_id(self, value):
        """Asserts validity of reviewer member during updates."""
        return self._validate_board_member(value, "reviewer")


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer to unpack and manage comment threads tied to tasks.

    Dynamically tracks comment authorship and returns string mappings for
    client consumption.
    """
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = [
            'id',
            'created_at',
            'author',
            'content',
        ]

    def get_author(self, obj):
        """Extracts the display name of the comment author."""
        return obj.author.fullname

    def create(self, validated_data):
        """
        Persists a new comment instance using standard validated parameters.
        """
        return Comments.objects.create(**validated_data)
