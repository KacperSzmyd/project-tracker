from django.urls import reverse


def test_users_see_only_their_projects_listed(
    auth_client_for_user, auth_client_for_user2, project
):
    url = reverse("project-list-create")

    resp1 = auth_client_for_user.get(url)
    assert resp1.status_code == 200

    # test with user1 authorized
    project_ids_user1 = [p["id"] for p in resp1.json()]
    assert project.id in project_ids_user1

    resp2 = auth_client_for_user2.get(url)
    project_ids_user2 = [p["id"] for p in resp2.json()]
    assert project.id not in project_ids_user2


def test_project_list_admin_sees_all(staff_client, project, project_with_two_members):
    url = reverse("project-list-create")
    response = staff_client.get(url)
    assert response.status_code == 200

    project_ids = [p["id"] for p in response.json()]
    assert len(project_ids) == 2


def test_project_create_auto_add_author(auth_client_for_user):
    url = reverse("project-list-create")
    response = auth_client_for_user.post(
        url, {"name": "Delta", "description": "X"}, format="json"
    )
    assert response.status_code == 201
    assert len(response.json()["members"]) == 1
    assert response.json()["members"][0]["username"] == "u1"


def test_project_detail_permission(
    api_client, auth_client_for_user, auth_client_for_user2, staff_client, project
):
    url = reverse("project-detail", kwargs={"pk": project.id})

    assert api_client.get(url).status_code == 401
    assert auth_client_for_user2.get(url).status_code == 403
    assert auth_client_for_user.get(url).status_code == 200
    assert staff_client.get(url).status_code == 200


def test_add_remove_member(auth_client_for_user, project, user2):
    add_url = reverse("add-member", kwargs={"pk": project.id})
    remove_url = reverse("remove-member", kwargs={"pk": project.id})

    # add
    resp1 = auth_client_for_user.post(add_url, {"user_id": user2.id}, format="json")
    assert resp1.status_code == 200

    # add already added member
    resp2 = auth_client_for_user.post(add_url, {"user_id": user2.id}, format="json")
    assert resp2.status_code == 409

    # remove
    resp3 = auth_client_for_user.delete(
        remove_url, {"user_id": user2.id}, format="json"
    )
    assert resp3.status_code == 200

