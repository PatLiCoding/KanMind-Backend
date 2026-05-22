from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Changes the default authentication identifier from 'username' to 'email'.
    The default 'username' field is made optional and non-unique, while a
    custom 'fullname' field is added.

    Attributes:
        fullname (str): The user's full first and last name (required).
        email (str): The unique email address used as the primary login
                    identifier.
        username (str): Optional username field, overridden from AbstractUser
                        to allow null values and non-unique entries.
    """
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150, unique=False, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        """
        Returns a string representation of the user, using their full name.
        """
        return self.fullname
