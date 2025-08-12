from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"], email=validated_data.get("email", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        source="assigned_to",
        queryset=User.objects.all(),
        write_only=True,
        required=False,
    )
    project_id = serializers.PrimaryKeyRelatedField(
        source="project", queryset=Project.objects.all(), write_only=True, required=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "assigned_to",
            "assigned_to_id",
            "project_id",
        ]

    def validate(self, attrs):
        project = attrs.get("project") or getattr(self.instance, "project", None)
        assignee = attrs.get("assigned_to")

        if assignee and project:
            is_member = project.members.filter(id=assignee.id).exists()
            if not is_member:
                raise serializers.ValidationError(
                    {"assigned_to_id": "Assignee must be a member of the project"}
                )
        return attrs


class ProjectSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at", "members", "tasks"]

    def create(self, validated_data):
        request = self.context.get("request")

        project = Project.objects.create(**validated_data)

        if request and request.user.is_authenticated:
            project.members.add(request.user)

        return project
