
import pytest

payload = {
    "email": "otisredding@gmail.com",
    "first_name": "Otis",
    "last_name": "Redding",
    "password": "secret",
    "password_confirmation": "secret"
}


def test_sign_up(client):
    res = client.post("/api/v1/users/register", json=payload)
    res_body = res.json()

    assert res_body["email"] == payload["email"]
    assert res.status_code == 201

def test_login(client, test_user):
    res = client.post("/api/v1/users/login", data={
        "username": test_user.get("email"),
        "password": test_user.get("password")
    })
    res_body = res.json()

    assert res.status_code == 200
    assert res_body["token"] is not None

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 401),
    ('otisredding@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('otisredding@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/api/v1/users/login", data={"username": email, "password": password})
    assert res.status_code == status_code
