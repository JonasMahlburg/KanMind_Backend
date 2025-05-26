from django.db import models

# Create your models here.
class Tasks(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    deadline = models.DateField(auto_now_add=True)
    prio = models.CharField(max_length=10)
    worked = models.CharField(max_length=100)

    def __str__(self):
             return f"{self.title}, {self.content}, ({self.deadline})"