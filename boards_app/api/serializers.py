from auth_app.models import User
from boards_app.models import Board
from rest_framework import serializers
from auth_app.api.serializers import UserMinimalSerializer
from tasks_app.api.serializers import TaskSerializer


class BoardSerializer(serializers.ModelSerializer):
    """
    Standard serializer for creating, listing, and updating Board instances.

    Includes computed read-only metrics about associated tasks and members.
    """
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
        """Calculates total number of members assigned to the board."""
        return obj.members.count()

    def get_ticket_count(self, obj):
        """Calculates total number of tasks attached to the board."""
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        """Calculates total number of tasks remaining in 'todo' status."""
        return obj.tasks.filter(status='todo').count()

    def get_tasks_high_prio_count(self, obj):
        """Calculates total number of tasks flagged with 'high' priority."""
        return obj.tasks.filter(priority='high').count()

    def create(self, validated_data):
        """Creates a board and populates its many-to-many relationship with
        members."""
        members = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members)
        return board

    def update(self, instance, validated_data):
        """
        Updates standard fields and overwrites the member list if provided.
        """
        members = validated_data.pop('members', None)
        instance = super().update(instance, validated_data)
        if members is not None:
            instance.members.set(members)
        return instance


class BoardDetailSerializer(serializers.ModelSerializer):
    """
    Detailed read-only serializer for a single Board instance.

    Expands relational IDs into full objects, nesting detailed member
    profiles and all child task objects.
    """
    members = UserMinimalSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            'id',
            'title',
            'owner_id',
            'members',
            'tasks'
        ]


class BoardMemberUpdateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer optimized for updating board titles and member
    lists.

    Accepts raw primary keys (IDs) for writes, but outputs nested, read-only
    structural objects for client rendering efficiency.
    """
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
        fields = [
            'id',
            'title',
            'members',
            'members_data',
            'owner_data'
        ]

    def update(self, instance, validated_data):
        """
        Performs the instance update safely checking for partial updates.

        Args:
            instance (Board): The existing board instance being modified.
            validated_data (dict): The dictionary of parsed incoming data.

        Returns:
            Board: The updated board instance.
        """
        if 'title' in validated_data:
            instance.title = validated_data.get(
                'title', instance.title)
        if 'members' in validated_data:
            instance.members.set(validated_data['members'])
        instance.save()
        return instance
