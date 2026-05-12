from django.db import models
from auth_app.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='owned_boards')
    member = models.ManyToManyField(
        User, related_name='boards')

    def __str__(self):
        return f"{self.title}"
