from rest_framework import serializers
from .models import Project, Task
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
        

class TaskSerializer(serializers.Serializer):
    assigned_to = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_at', 'assignedd_to']
        
        

class ProjectSerializer(serializers.Serializer):
    members = UserSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'members', 'tasks']