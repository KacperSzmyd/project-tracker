from django.urls import reverse


def test_create_only_member_can_create_tasks(
    auth_client_for_user, auth_client_for_user2, project, user2
):
    url = reverse("task-list")
    payload = {"title": "New", "project_id": project.id}

    # member
    resp1 = auth_client_for_user.post(url, payload, format="json")
    assert resp1.status_code == 201

    # not member
    resp2 = auth_client_for_user2.post(url, payload, format="json")
    assert resp2.status_code == 403

    # member creates task assigned to not member
    resp3 = auth_client_for_user.post(
        url,
        {"title": "X", "project_id": project.id, "assigned_to_id": user2.id},
        format="json",
    )
    assert resp3.status_code == 400


def test_assign_unassign_task_actions(task, auth_client_for_user, user, user2):
    assign_url = reverse("task-assign", kwargs={"pk": task.id})
    unassign_url = reverse("task-unassign", kwargs={"pk": task.id})

    # unassign
    resp1 = auth_client_for_user.patch(
        unassign_url, {"user_id": user.id}, format="json"
    )
    assert resp1.status_code == 200
    task.refresh_from_db()
    assert task.assigned_to_id is None

    # assign
    resp2 = auth_client_for_user.patch(assign_url, {"user_id": user.id}, format="json")
    assert resp2.status_code == 200
    task.refresh_from_db()
    assert task.assigned_to == user

    # assign invalid member
    resp3 = auth_client_for_user.patch(assign_url, {"user_id": user2.id}, format="json")
    assert resp3.status_code == 400

    # unassign invalid member
    resp4 = auth_client_for_user.patch(
        unassign_url, {"user_id": user2.id}, format="json"
    )
    assert resp4.status_code == 400


def test_set_status_action(
    task, auth_client_for_user, auth_client_for_user2, staff_client
):
    url = reverse("task-set-status", kwargs={"pk": task.id})

    # valid member
    resp1 = auth_client_for_user.patch(url, {"status": "IN_PROGRESS"}, format="json")
    assert resp1.status_code == 200
    task.refresh_from_db()
    assert task.status == "IN_PROGRESS"

    # invalid member
    resp2 = auth_client_for_user2.patch(url, {"status": "DONE"}, format="json")
    assert resp2.status_code == 404

    # admin
    resp3 = staff_client.patch(url, {"status": "DONE"}, format="json")
    assert resp3.status_code == 200
    task.refresh_from_db()
    assert task.status == "DONE"
