from django.urls import reverse


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


def test_user_delete_admin_only(staff_client, api_client, user):
    url = reverse("delete-user", kwargs={"pk": user.id})
    assert api_client.delete(url).status_code in (401, 403)

    assert staff_client.delete(url).status_code == 204
