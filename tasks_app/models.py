from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



# Create your models here.
class Tasks(models.Model):
    
    """
    Represents a task in the Kanmind application.

    Attributes:
        STATUS_CHOICES (list): A list of possible status choices for the task.

        title (CharField): The title of the task, with a maximum length of 100 characters.
        content (TextField): A short description of the task, limited to 150 characters.
        date (DateTimeField): The date and time the task was last modified. 
            Automatically set to the current time on each save.
        deadline (DateField): The optional deadline for the task.
        prio (CharField): The priority level of the task. Expected values are 
            'critical', 'high', 'medium', or 'low'.
        owner (ForeignKey): The user who created the task. If the user is deleted, 
            the task will remain with a null owner.
        worked (ManyToManyField): A list of users who are assigned to work on the task.
        board (ForeignKey): The board to which this task belongs. Deleting the board 
            will also delete all its associated tasks.
        status (CharField): The current status of the task, with possible choices defined 
            in STATUS_CHOICES. Defaults to 'to-do'.

    Meta:
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.

    Methods:
        __str__(): Returns a string representation of the task, including the title,
        content, and deadline.
    """

    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('reviewing', 'Reviewing'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    deadline = models.DateField(blank=True, null=True)
    prio = models.CharField(max_length=10, help_text="please use: 'critical', 'high', 'medium' or 'low'")
    owner = models.ForeignKey(
            get_user_model(),
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='created_tasks',
            help_text="Der User, der den Task erstellt hat"
    )
    worked = models.ManyToManyField(User, related_name='assignee')
    board = models.ForeignKey('boards_app.Boards', on_delete=models.CASCADE, related_name='tasks'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='to-do'
    )
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
             return f"{self.title}, {self.content}, ({self.deadline})"
    
class Comment(models.Model):
    """
    Represents a comment made by a user on a task.

    Attributes:
        task (ForeignKey): A reference to the related task. When the task is deleted,
            all associated comments will be deleted as well.
        text (TextField): The content of the comment, limited to 300 characters.
        author (ForeignKey): The user who wrote the comment. When the user is deleted,
            all associated comments will be deleted.
        created_at (DateTimeField): The date and time when the comment was created.
            This field is automatically set when the comment is created.

    Meta:
        verbose_name (str): Human-readable singular name for the model.
        verbose_name_plural (str): Human-readable plural name for the model.

    Methods:
        __str__(): Returns a human-readable string representation of the comment,
            showing which user wrote it and its associated task.
    """
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(max_length=300)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return f"The comment on '{self.task.title}' is written by {self.author}"
    
    