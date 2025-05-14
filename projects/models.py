from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.name.title()


class Task(models.Model):
    STATUS_CHOICES = {
        "TODO": "Do zrobienia",
        "IN_PROGRESS": "W trakcie",
        "DONE": "Zrobione",
    }
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL, related_name="tasks"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="TODO")
    due_date = models.DateField(blank=True, null=True)
    createdd_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} @{self.status}"
