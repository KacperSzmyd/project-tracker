from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Task, Project


class CustomUserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(Task)
admin.site.register(Project)
