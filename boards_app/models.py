from django.db import models
from django.conf import settings

class Boards(models.Model):
    title = models.CharField(max_length=255)
    member_count = models.PositiveIntegerField(default=0)
    ticket_count = models.PositiveIntegerField(default=0)
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

    def __str__(self):
        return self.title

    @property
    def tasks_to_do_count(self):
        return self.tasks.filter(status='to_do').count()

    @property
    def tasks_high_prio_count(self):
        return self.tasks.filter(status='to_do', priority='high').count()
