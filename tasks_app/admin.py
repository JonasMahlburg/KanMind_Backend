from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    list_display = ('title',  'priority', 'due_date')
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "description", "due_date", "priority", "board"],
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