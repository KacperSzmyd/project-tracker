import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_jwt_flow(api_client):
    # register
    register = api_client.post(
        reverse("user-register"), {"username": "jwtuser", "password": "pass12345"}
    )
    assert register.status_code == 201

    # obtain token
    token_response = api_client.post(
        reverse("token-obtain-pair"),
        {"username": "jwtuser", "password": "pass12345"},
        format="json",
    )
    assert token_response.status_code == 200
    access = token_response.json()["access"]

    # call protected endpoint
    response = api_client.get(
        reverse("project-list-create"), HTTP_AUTHORIZATION=f"Bearer {access}"
    )
    assert response.status_code == 200
