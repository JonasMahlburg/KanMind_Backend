from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
        list_display = ["title", "role", "department"]

# Register your models here.
admin.site.register(User)