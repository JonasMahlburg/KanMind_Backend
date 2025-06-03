from django.db import models
from django.conf import settings
from tasks_app.models import Tasks
from user_auth_app.models import User

class Boards(models.Model):
    title = models.CharField(max_length=255)
    member_count = models.ManyToManyField(User, related_name='boards_member_count')
    tasks_to_do_count = models.ManyToManyField(
        Tasks,
        related_name='boards_with_this_task',
        limit_choices_to={'status': 'to-do'}
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards',
        blank=True
    )

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
   
    @property
    def tasks_to_do_count(self):
        return self.tasks.filter(status='to-do').count()
    
    def __str__(self):
        return self.title
