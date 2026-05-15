from auth_app.models import User
from boards_app.models import Board
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer


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


class BoardDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'members',
            'tasks'
        ]

    def get_members(self, obj):
        return [
            {
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
            }
            for user in obj.members.all()
        ]


class BoardMemberUpdateSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True
    )
    members_data = UserMinimalSerializer(
        source='members',
        many=True,
        read_only=True
    )
    owner_data = UserMinimalSerializer(source='owner', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'members_data', 'owner_data']

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            instance.title = validated_data['title']
        if 'members' in validated_data:
            instance.members.set(validated_data['members'])
        instance.save()
        return instance
