from auth_app.models import User
from boards_app.models import Board
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    member = serializers.ListField(
        child=serializers.EmailField(),
        write_only=True,
        required=False
    )
    owner_id = serializers.ReadOnlyField(
        source='owner.id'
    )
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'member',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count'
        ]

    def get_member_count(self, obj):
        return obj.member.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='todo').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    def validate_members(self, value):
        users = []
        for email in value:
            try:
                user = User.objects.get(email=email)
                users.append(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    f"User mit Email {email} existiert nicht."
                )
        return users

    def create(self, validated_data):
        member = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        if member:
            board.member.set(member)
        return board
