import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_success():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Ensure not already signed up
    client.get("/activities")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_for_activity_duplicate():
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_signup_for_nonexistent_activity():
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
