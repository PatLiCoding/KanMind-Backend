from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Changes the default authentication identifier from 'username' to 'email'
    and adds additional profile fields.

    Attributes:
        fullname (str): The user's full first and last name.
        email (str): The unique email address used as the primary login
        identifier.
    """
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname']

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return self.fullname
