from django.db import models
from auth_app.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='owner')
    member = models.ManyToManyField(
        User, related_name='members')
    member_count = models.IntegerField(default=0)
    ticket_count = models.IntegerField(default=0)
    tasks_to_do_count = models.IntegerField(default=0)
    tasks_high_prio_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}"
