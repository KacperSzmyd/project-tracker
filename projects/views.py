from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from .models import Project, Task
from .serializers import (
    ProjectSerializer,
    TaskSerializer,
    UserRegisterSerializer,
    UserSerializer,
)
from .permissons import IsProjectMember
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "pk"


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


class ProjectListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.user.is_staff:
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(members=request.user)

        projects = projects.prefetch_related("members", "tasks").distinct()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailApiView(APIView):
    permission_classes = [IsAuthenticated, IsProjectMember]

    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        serializer = ProjectSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        self.check_object_permissions(request, project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_user_to_project(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response(
            {"error": "Project does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    if not (request.user.is_staff or request.user in project.members.all()):
        return Response(
            {"error": "You are not allowed to add members"},
            status=status.HTTP_403_FORBIDDEN,
        )

    username = request.data.get("username")

    try:
        user_to_add = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    project.members.add(user_to_add)
    return Response(
        {"message": f"User {username} added to project {project.name}"},
        status=status.HTTP_200_OK,
    )
