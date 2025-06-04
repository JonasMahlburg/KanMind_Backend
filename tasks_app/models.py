from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User



# Create your models here.
class Tasks(models.Model):
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
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")

    def __str__(self):
        return f"The Comments {self.title} is written by {self.author}"
    
    