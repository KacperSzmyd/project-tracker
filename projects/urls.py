from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectDetailApiView, ProjectListCreateApiView, TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("projects", ProjectListCreateApiView.as_view(), name="project-list-create"),
    path("projects/<int:pk>", ProjectDetailApiView.as_view(), name="project-detail"),
]
