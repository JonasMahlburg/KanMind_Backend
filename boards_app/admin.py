from django.contrib import admin
from .models import Boards

class BoardsAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Boards model.

    This class defines how Boards are displayed and edited in the Django admin.

    Attributes:
        list_display (tuple): Specifies the fields to display in the list view.
        fieldsets (list): Defines how fields are grouped and displayed in the form view.

    Methods:
        tasks_to_do_count_display(obj): Returns the number of tasks to do for the given board.
        member_count_display(obj): Returns the number of members in the given board.
    """
    list_display = ('title', 'member_count_display', 'tasks_to_do_count_display')
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "member_count", "tasks_to_do_count_display"],
            },
        ),
        (
            "more",
            {
                "classes": ["collapse"],
                "fields": ["owner", "members"],
            },
        ),
    ]

    def tasks_to_do_count_display(self, obj):
        """
        Return the number of tasks to do for the given board.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: The number of tasks marked as "to-do".
        """
        return obj.tasks_to_do_count
    tasks_to_do_count_display.short_description = 'Tasks To Do'

    def member_count_display(self, obj):
        """
        Return the number of members for the given board.

        Args:
            obj (Boards): The board instance.

        Returns:
            int: The number of users assigned as members of the board.
        """
        return obj.members.count()
    member_count_display.short_description = 'Mitgliederzahl'
