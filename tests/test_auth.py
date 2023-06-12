from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)

payload = {
    "email": "otisredding@gmail.com",
    "first_name": "Otis",
    "last_name": "Redding",
    "password": "secret",
    "password_confirmation": "secret"
}


def test_read_main():
    res = client.post("/api/v1/users/register", json=payload)
    res_body = res.json()

    assert res_body["email"] == payload["email"]
    assert res.status_code == 201