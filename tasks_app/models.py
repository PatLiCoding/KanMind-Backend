from django.db import models
from boards_app.models import Board
from auth_app.models import User


# Create your models here.


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('review', 'Review'),
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
    assignee = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tasks'
    )
    reviewer = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_tasks'
    )
    due_date = models.DateField()
    create_by = models.ForeignKey(User, related_name='created_tasks',
        on_delete=models.SET_NULL,null=True)
    
    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return self.title


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, 
        related_name='comments')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author} on {self.task.title}"
