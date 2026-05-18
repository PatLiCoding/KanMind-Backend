from auth_app.models import User
from tasks_app.models import Task, Comments
from boards_app.models import Board
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


class TaskSerializer(serializers.ModelSerializer):
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
        return obj.comments.count()
    
    def _validate_board_member(self, user, field_name):
        if not user:
            return None
        try:
            board = self.initial_data.get('board') or (
                self.instance.board.id if self.instance else None)
            board_obj = Board.objects.get(id=board)
            if not (board_obj.owner == user or 
                    board_obj.members.filter(id=user.id).exists()):
                raise serializers.ValidationError(
                    f"The selected {field_name} is not a member of this board.")
            return user
        except Board.DoesNotExist:
            raise serializers.ValidationError("Invalid board ID.")

    def validate_assignee_id(self, value):
        return self._validate_board_member(value, "assignee")

    def validate_reviewer_id(self, value):
        return self._validate_board_member(value, "reviewer")
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['create_by'] = request.user
        comments = validated_data.pop('comments', [])
        task = Task.objects.create(**validated_data)
        task.create_by = request.user
        task.comments.set(comments)
        return task
    

class TaskDetailSerializer(serializers.ModelSerializer):
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
        if not user:
            return user
        board_id = self.initial_data.get('board') or (
            self.instance.board.id if self.instance else None)
        if not board_id:
            raise serializers.ValidationError("Board ID is required.")  
        try:
            board_obj = Board.objects.get(id=board_id)
            if not (board_obj.owner == user or 
                    board_obj.members.filter(id=user.id).exists()):
                raise serializers.ValidationError(
                    f"The selected {field_name} is not a member of this board.")
        except Board.DoesNotExist:
            raise serializers.ValidationError("Invalid board ID.")
        return user

    def validate_assignee_id(self, value):
        return self._validate_board_member(value, "assignee")

    def validate_reviewer_id(self, value):
        return self._validate_board_member(value, "reviewer")
    

class CommentsSerializer(serializers.ModelSerializer):
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
        return obj.author.fullname

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)