import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdHJpbmcxQHlhaG9vLmNvbSIsImlhdCI6MTY4NjYwMzgxNSwibmJmIjoxNjg2NjAzODE1LCJqdGkiOiI0MGZlNjg5YS1iOGJjLTQ3MTItYTgzYS1iZGE2YTk0ZmEyMjYiLCJleHAiOjE2ODY2MDQ3MTUsInR5cGUiOiJhY2Nlc3MiLCJmcmVzaCI6ZmFsc2V9.WdJsdlSjDpBgka2KOBM-_A2fLvXR6rUCWgvXuSmKX5M"


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {token}"}


def test_create_entry(auth_headers):
    payload = {"text": "rice", "calories": 200}
    response = client.post("/api/v1.0/new_entry", headers=auth_headers, json=payload)
    assert response.status_code == 201
    response_body = response.json()
    assert response_body.get("message") == "New entry created"
   
    


def test_get_all_entries(auth_headers):
    response = client.get("/api/v1.0/all_entries", headers=auth_headers)
    assert response.status_code == 200
   
    


def test_get_total_calories(auth_headers):
  

    response = client.get("/api/v1.0/total_calories", headers=auth_headers)
    assert response.status_code == 200
    
    


