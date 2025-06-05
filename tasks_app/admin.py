from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    list_display = ('id','title',  'priority', 'due_date')
    fieldsets = [
        (
            None,
            {
                "fields": [ "id","title", "content", "due_date", "priority"],
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