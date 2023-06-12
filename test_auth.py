import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


@pytest.fixture(scope="module")
def test_user():
    return {
        "email": "test11@example.com",
        "password": "testpassword",
        "role": "user"
    }


def test_new_user_registration(test_user):
    response = client.post("/api/v1.0/sign_up", json=test_user)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "New user created"}


def test_user_login(test_user):
    response = client.post("/api/v1.0/sign_in", json=test_user)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

def test_incorrect_password_login(test_user):
    incorrect_password_user = test_user.copy()
    incorrect_password_user["password"] = "incorrectpassword"
    response = client.post("/api/v1.0/sign_in", json=incorrect_password_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST




