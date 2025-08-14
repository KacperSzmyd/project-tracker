import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from projects.models import Task, Project


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create(username="u1", password="pass123")


@pytest.fixture
def user2(db):
    return User.objects.create(username="u2", password="pass123")


@pytest.fixture
def staff(db):
    u = User.objects.create(username="admin", password="pass123", email="a@a.com")
    u.is_staff = True
    u.save()

    return u


@pytest.fixture
def auth_client_for_user(user):
    authenticated_client = APIClient()
    authenticated_client.force_authenticate(user=user)
    return authenticated_client


@pytest.fixture
def auth_client_for_user2(user2):
    authenticated_client = APIClient()
    authenticated_client.force_authenticate(user=user2)
    return authenticated_client


@pytest.fixture
def staff_client(staff):
    client_for_staff = APIClient()
    client_for_staff.force_authenticate(user=staff)
    return client_for_staff


@pytest.fixture
def project(db, user):
    p = Project.objects.create(name="Alpha", description="demo")
    p.members.add(user)
    return p


@pytest.fixture
def project_with_two_members(project, user, user2):
    p = Project.objects.create(name="Beta", description="Project with two members")
    p.members.add(user)
    p.members.add(user2)
    return p


@pytest.fixture
def task(db, project, user):
    return Task.objects.create(project=project, title="T1", assigned_to=user)
