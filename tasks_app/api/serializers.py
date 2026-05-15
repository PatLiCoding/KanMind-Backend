from auth_app.models import User
from tasks_app.models import Task
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 
            'priority', 'assignees', 'reviewers', 'due_date'
        ]
