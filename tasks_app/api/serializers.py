from auth_app.models import User
from tasks_app.models import Task, Comments
from boards_app.models import Board
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    create_by = UserMinimalSerializer(write_only=True)
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
            'assignees', 'reviewer_id', 'reviewers',
            'due_date', 'comments', 'comments_count',
            'create_by'
        ]
        
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def _validate_board_member(self, user_id, field_name):
        if not user_id:
            return None
        try:
            user = User.objects.get(id=user_id)
            board = self.initial_data.get('board')
            board_obj = Board.objects.get(id=board)
            if not (board_obj.owner == user or 
                    board_obj.members.filter(id=user.id).exists()):
                raise serializers.ValidationError(
                    f"The selected {field_name} is not a member of this board.")
            return user
        except (User.DoesNotExist, Board.DoesNotExist):
            raise serializers.ValidationError(f"Invalid {field_name} or board ID.")

    def validate_assignee_id(self, value):
        return self._validate_board_member(value, "assignee")

    def validate_reviewer_id(self, value):
        return self._validate_board_member(value, "reviewer")
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['create_by'] = request.user
        assignee = validated_data.pop('assignee_id', None)
        reviewer = validated_data.pop('reviewer_id', None)
        comments = validated_data.pop('comments', [])
        task = Task.objects.create(**validated_data)
        if assignee: task.assignees.add(assignee)
        if reviewer: task.reviewers.add(reviewer)
        task.comments.set(comments)
        return task

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['assignees'] = UserMinimalSerializer(instance.assignees.all(), many=True).data
        representation['reviewers'] = UserMinimalSerializer(instance.reviewers.all(), many=True).data
        representation.pop('assignee_id', None)
        representation.pop('reviewer_id', None)
        return representation
    