from django.db import models
from django.conf import settings
from tasks_app.models import Tasks
from user_auth_app.models import User


class Boards(models.Model):
    """
    Represents a board within the Kanmind application.

    A board serves as a container for tasks and can have multiple members.
    Only tasks with the status 'to-do' can be assigned via the tasks_to_do relationship.

    Attributes:
        title (CharField): The title or name of the board.
        tasks_to_do (ManyToManyField): Tasks associated with this board, limited to tasks with status 'to-do'.
        owner (ForeignKey): The user who owns the board. Deleting the user will also delete the board.
        members (ManyToManyField): Users who are members of the board. Can be empty.

    Meta:
        verbose_name (str): Human-readable name for a single board.
        verbose_name_plural (str): Human-readable name for multiple boards.

    Methods:
        __str__(): Returns the board title as its string representation.
    """
    title = models.CharField(max_length=255)
  
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
        """
        Return the string representation of the board.

        Returns:
            str: The title of the board.
        """
        return self.title
