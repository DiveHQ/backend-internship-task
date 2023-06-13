from src.schema.calories import Calorie

calorie_entry = {"text": "rice", "number_of_calories": 100}


def test_create_calorie_entry(authorized_user):
    client, _ = authorized_user
    res = client.post("/api/v1/calories", json=calorie_entry)
    res_body = res.json()

    assert res.status_code == 201
    assert res_body.get("text") == calorie_entry.get("text")
    assert res_body.get("number_of_calories") == calorie_entry.get("number_of_calories")


def test_get_all_calorie_entries(authorized_user, calorie_entries):
    client, user = authorized_user
    res = client.get("/api/v1/calories")
    current_user_entries = [
        entry for entry in calorie_entries if entry.user_id == user.get("id")
    ]
    calories = res.json()

    assert len(calories["calorie_entries"]) == len(current_user_entries)
    assert res.status_code == 200


def test_get_one_calorie_entry(authorized_user, calorie_entries):
    client, _ = authorized_user
    res = client.get(f"/api/v1/calories/{calorie_entries[0].id}")
    calorie = Calorie(**res.json())

    assert calorie.id == calorie_entries[0].id
    assert calorie.date == calorie_entries[0].date
    assert calorie.time == calorie_entries[0].time
    assert calorie.number_of_calories == calorie_entries[0].number_of_calories
    assert res.status_code == 200


# def test_delete
