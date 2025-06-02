from django.contrib import admin
from .models import Boards

class BoardsAdmin(admin.ModelAdmin):
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
        return obj.tasks_to_do_count
    tasks_to_do_count_display.short_description = 'Tasks To Do'

    def member_count_display(self, obj):
        return obj.members.count()
    member_count_display.short_description = 'Mitgliederzahl'

# Register your models here.
admin.site.register(Boards, BoardsAdmin)
