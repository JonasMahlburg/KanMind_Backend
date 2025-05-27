from django.contrib import admin
from .models import Tasks

class TasksAdmin(admin.ModelAdmin):
    list_display = ('title',  'prio', 'deadline')
    fieldsets = [
        (
            None,
            {
                "fields": ["title", "content", "deadline", "prio"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["worked"],
            },
        ),
    ]

# Register your models here.
admin.site.register(Tasks, TasksAdmin)