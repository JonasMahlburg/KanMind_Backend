from django.db import models

# Create your models here.
class Boards(models.Model):
     title = models.CharField(max_length=50)
     member_count = models.FloatField(("memeber"))
     ticket_count = models.FloatField(("ticket"))
     tasks_to_do_count = models.FloatField(("ticket"))
     tasks_high_prio_count = models.FloatField(("ticket"))
     owner_id = models.FloatField(("ticket"))
    
    
     class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'

     def __str__(self):
             return f"{self.title}, {self.member_count}, ({self.tasks_to_do_count})"
    # "member_count": 2,
    # "ticket_count": 5,
    # "tasks_to_do_count": 2,
    # "tasks_high_prio_count": 1,
    # "owner_id": 12
    