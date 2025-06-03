from django.db import models


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
    deadline = models.DateField(blank=True)
    prio = models.CharField(max_length=10, help_text="please use: 'critical', 'high', 'medium' or 'low'")
    worked = models.CharField(max_length=100)
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