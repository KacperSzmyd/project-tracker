from rest_framework.test import APIClient
from django.urls import reverse
import pytest


def test_user_register_open(api_client, db):
    url = reverse("user-register")
    response = api_client.post(
        url, {"username": "newbie", "password": "pass12345"}, format="json"
    )
    assert response.status_code == 201


def test_user_list_requires_admin(api_client, staff_client):
    url = reverse("users-list")

    assert api_client.get(url).status_code in (401, 403)

    assert staff_client.get(url).status_code == 200


def test_user_delete_admin_only(client, staff, user):
    client = APIClient()

    url = reverse("delete-user", kwargs={"pk": user.id})
    assert client.delete(url).status_code in (401, 403)

    client.force_authenticate(user=staff)
    assert client.delete(url).status_code == 204
