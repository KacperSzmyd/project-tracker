from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "assignedd_to",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at", "members", "tasks"]

    def create(self, validated_data):
        members_data = validated_data.pop("members", [])
        request = self.context.get("request")

        project = Project.objects.create(**validated_data)

        if request and request.user.is_authenticated:
            project.members.add(request.user)

        for member in members_data:
            project.members.add(member)

        return project
