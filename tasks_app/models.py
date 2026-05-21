from django.db import models
from boards_app.models import Board
from auth_app.models import User


# Create your models here.


class Task(models.Model):
    """
    Represents an item of work assigned within a specific Board tracking
    environment.

    Tracks implementation state, priorities, responsible profiles, and
    delivery timelines.

    Attributes:
        board (ForeignKey): Structural workspace where this task resides.
        title (str): The concise task summary.
        description (str): Detailed steps or criteria required to resolve the
                            task.
        status (str): The active phase of the task (e.g., todo, inprogress,
                        review, done).
        priority (str): Level of operational urgency (low, medium, high).
        assignee (ForeignKey): User actively implementing the requirements.
        reviewer (ForeignKey): User responsible for QA auditing and approval
                                signs.
        due_date (DateField): Calendar target completion limit.
        create_by (ForeignKey): Record of the user who initially initialized
                                this task instance.
    """
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
                                  on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        """Returns the task's text title representation."""
        return self.title


class Comments(models.Model):
    """
    Represents an atomic feedback or discussion post appended to a Task.

    Attributes:
        created_at (DateTimeField): Log recording precisely when the message
                                    entry cleared.
        author (ForeignKey): Profile reference linking back to the commenter.
        task (ForeignKey): Core task instance tracking the parent thread
                            context.
        content (str): The raw text message payload.
    """
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
        """
        Returns a compiled display description specifying author identity
        and context.
        """
        return f"Comment by {self.author} on {self.task.title}"
