from django.db import models

# Create your models here.
class Boards(models.Model):
     title = models.CharField(max_length=50)
     # member_count
    # "member_count": 2,
    # "ticket_count": 5,
    # "tasks_to_do_count": 2,
    # "tasks_high_prio_count": 1,
    # "owner_id": 12
    