from auth_app.models import User
from boards_app.models import Board
from rest_framework import serializers


class BoardSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False)
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
            'members',
            'member_count',
            'ticket_count',
            'tasks_to_do_count',
            'tasks_high_prio_count',
            'owner_id',
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='todo').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()

    def validate_member(self, value):
        users = User.objects.filter(email__in=value)
        if len(users) != len(value):
            existing_emails = users.values_list('email', flat=True)
            missing = set(value) - set(existing_emails)
            raise serializers.ValidationError(
                f"User with email '{list(missing)}' does not exist.")
        return users

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        return board

    def update(self, instance, validated_data):
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
        return instance
