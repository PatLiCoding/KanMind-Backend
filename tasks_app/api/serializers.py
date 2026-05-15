from auth_app.models import User
from tasks_app.models import Task, Comments
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


class TaskSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(
        queryset= Comments.objects.all(),
        many=True,
        write_only=True,
        required=False)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 
            'priority', 'assignees', 'reviewers', 'due_date',
            'comments', 'comments_count']
        
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def create(self, validated_data):
        comments = validated_data.pop('comments', [])
        task = Task.objects.create(**validated_data)
        task.comments.set(comments)
        return task
    

