import copy

from src.app import activities


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200

    payload = response.json()
    assert len(payload) == 9
    assert "Chess Club" in payload
    assert payload["Chess Club"]["max_participants"] == 12
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_participant(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    starting_participants = copy.deepcopy(activities[activity_name]["participants"])

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert activities[activity_name]["participants"] == starting_participants + [email]


def test_signup_for_activity_rejects_duplicate_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    starting_participants = copy.deepcopy(activities[activity_name]["participants"])

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }
    assert activities[activity_name]["participants"] == starting_participants


def test_signup_for_missing_activity_returns_404(client):
    response = client.post(
        "/activities/Robotics Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    starting_participants = copy.deepcopy(activities[activity_name]["participants"])

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }
    assert activities[activity_name]["participants"] == [
        participant for participant in starting_participants if participant != email
    ]


def test_unregister_from_activity_rejects_missing_participant(client):
    activity_name = "Chess Club"
    email = "absent.student@mergington.edu"
    starting_participants = copy.deepcopy(activities[activity_name]["participants"])

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
    assert activities[activity_name]["participants"] == starting_participants


def test_unregister_from_missing_activity_returns_404(client):
    response = client.delete(
        "/activities/Robotics Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}