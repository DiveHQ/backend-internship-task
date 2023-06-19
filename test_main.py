import pytest
from fastapi.testclient import TestClient
from main import app
from datetime import date, time
from unittest.mock import Mock, patch
from main import fetch_calories_from_api
all_entries = []
client = TestClient(app)

def test_create_entry():
    entry_data = {
        "date": str(date.today()),
        "time": str(time(12, 0)),
        "text": "Test entry",
        "calories": 500
    }
    response = client.post("/api/entries", json=entry_data,auth=('asifxy', 'pass'))
    assert response.status_code == 200
    assert response.json() == {"message": "Entry created successfully"}

def test_get_entries():
    global all_entries
    response = client.get("/api/entries",auth=('asifxy', 'pass'))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    all_entries = [entry["id"] for entry in response.json()]

def test_get_entry():
    response = client.get(f"/api/entries/{all_entries[0]}",auth=('asifxy', 'pass'))
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_entry():
    updated_entry_data = {
        "date": str(date.today()),
        "time": str(time(14, 0)),
        "text": "Updated entry",
        "calories": 600
    }
    response = client.put(f"/api/entries/{all_entries[0]}", json=updated_entry_data,auth=('asifxy', 'pass'))
    assert response.status_code == 200
    assert response.json() == {"message": "Entry updated successfully"}

def test_delete_entry():
    response = client.delete(f"/api/entries/{all_entries[0]}",auth=('asifxy', 'pass'))
    assert response.status_code == 200
    assert response.json() == {"message": "Entry deleted successfully"}

def test_create_entry_missing_fields():
    entry_data = {}
    response = client.post("/api/entries", json=entry_data,auth=('asifxy', 'pass'))
    assert response.status_code == 422  

def test_get_entry_not_found():
    response = client.get("/api/entries/999",auth=('asifxy', 'pass'))
    assert response.status_code == 404

def test_update_entry_not_found():
    updated_entry_data = {
        "date": str(date.today()),
        "time": str(time(14, 0)),
        "text": "Updated entry",
        "calories": 600
    }
    response = client.put("/api/entries/999", json=updated_entry_data,auth=('asifxy', 'pass'))
    assert response.status_code == 404

def test_delete_entry_not_found():
    response = client.delete("/api/entries/999",auth=('asifxy', 'pass'))
    assert response.status_code == 404 


def test_fetch_calories_from_api_successful():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "branded": [
            {
                "nf_calories": 300
            }
        ]
    }

    with patch('requests.get', return_value=mock_response):
        calories = fetch_calories_from_api("meal")
        assert calories == 300

def test_fetch_calories_from_api_no_branded_food():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "branded": []
    }

    with patch('requests.get', return_value=mock_response):
        calories = fetch_calories_from_api("meal")
        assert calories is None

def test_fetch_calories_from_api_error():
    mock_response = Mock()
    mock_response.status_code = 500

    with patch('requests.get', return_value=mock_response):
        calories = fetch_calories_from_api("meal")
        assert calories is None