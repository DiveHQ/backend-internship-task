from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from src.db.database import Base, get_db
from src.main import app
from datetime import datetime, time
from src.db import models

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user = {
        "email": "otisredding@gmail.com",
        "first_name": "Otis",
        "last_name": "Redding",
        "password": "secret",
        "password_confirmation": "secret",
    }
    res = client.post("/api/v1/users/register/", json=user)

    assert res.status_code == 201
    new_user = res.json()
    new_user["data"]["password"] = user.get("password")
    new_user["data"]["id"] = 1
    return new_user


@pytest.fixture
def test_user_1(client):
    user = {
        "email": "arethafranklin@gmail.com",
        "first_name": "Aretha",
        "last_name": "Franklin",
        "password": "secret",
        "password_confirmation": "secret",
    }
    res = client.post("/api/v1/users/register/", json=user)

    assert res.status_code == 201
    new_user = res.json()
    new_user["data"]["password"] = user.get("password")
    new_user["data"]["id"] = 2
    return new_user


@pytest.fixture
def authorized_user(client, test_user):
    res = client.post(
        "/api/v1/users/login",
        data={
            "username": test_user.get('data').get("email"),
            "password": test_user.get('data').get("password"),
        },
    )
    res_body = res.json()
    token = res_body.get("data").get("token")
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}

    return client, test_user


def return_calorie(entry):
    return models.CalorieEntry(**entry)


@pytest.fixture
def calorie_entries(test_user, session, test_user_1):
    date = datetime.now().date()
    datetime_time = datetime.now().time()
    time_obj = time(
        datetime_time.hour,
        datetime_time.minute,
        datetime_time.second,
        datetime_time.microsecond,
    )

    calories = [
        {
            "text": "beef",
            "id": 1,
            "is_below_expected": True,
            "user_id": test_user.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 90,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "text": "chicken",
            "id": 2,
            "is_below_expected": True,
            "user_id": test_user_1.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 70,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "text": "rice",
            "id": 3,
            "is_below_expected": True,
            "user_id": test_user.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 70,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "text": "grape",
            "id": 4,
            "is_below_expected": True,
            "user_id": test_user_1.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 150,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "text": "milo",
            "id": 5,
            "is_below_expected": False,
            "user_id": test_user.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 660,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
        {
            "text": "water",
            "id": 6,
            "is_below_expected": False,
            "user_id": test_user_1.get("data").get("id"),
            "date": date,
            "time": time_obj,
            "number_of_calories": 70,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        },
    ]

    entry = map(return_calorie, calories)
    calorie_entries = list(entry)

    session.add_all(calorie_entries)

    session.commit()

    saved_entries = session.query(models.CalorieEntry).all()

    return saved_entries
