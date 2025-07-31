from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectDetailApiView,
    ProjectListCreateApiView,
    TaskViewSet,
    UserRegisterView,
    UserListView,
    add_user_to_project,
    remove_member_from_project,
    UserDeleteView,
)


router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/register/", UserRegisterView.as_view(), name="user-register"),
    path("users/delete/<int:pk>/", UserDeleteView.as_view(), name="delete-user"),
    path("projects/", ProjectListCreateApiView.as_view(), name="project-list-create"),
    path("projects/<int:pk>/", ProjectDetailApiView.as_view(), name="project-detail"),
    path("projects/<int:pk>/add-member/", add_user_to_project, name="add-member"),
    path("projects/<int:pk>/remove-member/", remove_member_from_project, name="remove-member"),
]
