from django.db import models
from auth_app.models import User

# Create your models here.


class Board(models.Model):
    """
    Represents a project or task board within the system.

    A board acts as a workspace that has one clear owner and can be
    shared across multiple contributing users (members).

    Attributes:
        title (str): The alphanumeric display title of the board.
        owner (ForeignKey): Reference to the User who administers the board.
                            Set to NULL if the user is deleted.
        members (ManyToManyField): Collection of approved Users who have shared
                                   access permissions to view and modify the
                                   board.
    """
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='owned_boards')
    members = models.ManyToManyField(
        User, related_name='boards')

    def __str__(self):
        """
        Returns the string identifier of the board.
        """
        return f"{self.title}"
