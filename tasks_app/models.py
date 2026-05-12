from django.db import models
from boards_app.models import Board

# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField(default="No description available.")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default='medium')
