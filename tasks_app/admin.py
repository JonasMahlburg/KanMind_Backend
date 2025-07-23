from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    list_display = ('title',  'priority', 'due_date')
    fieldsets = [
        (
            None,
            {
                "fields": ['id', "title", "description", "due_date", "priority", "board_id"],
            },
        ),
        (
            "Co-workers",
            {
                "classes": ["collapse"],
                "fields": ["assignee"],
            },
        ),
    ]

# Register your models here.
admin.site.register(Tasks, TasksAdmin)