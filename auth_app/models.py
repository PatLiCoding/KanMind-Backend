from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager for the custom user model that uses email instead of a username.
    """

    def create_user(self, email, fullname, password=None, **extra_fields):
        if not email:
            raise ValueError('An email address is mandatory.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fullname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must is_superuser=True.')
        return self.create_user(email, fullname, password, **extra_fields)


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
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        """
        Returns a string representation of the user, using their full name.
        """
        return self.fullname
