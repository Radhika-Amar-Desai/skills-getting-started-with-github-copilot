import urllib.parse


def test_get_activities(app_client):
    res = app_client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_success(app_client):
    email = "tester@example.com"
    res = app_client.post("/activities/Programming%20Class/signup", params={"email": email})
    assert res.status_code == 200
    data = app_client.get("/activities").json()
    assert email in data["Programming Class"]["participants"]


def test_signup_duplicate(app_client):
    email = "dup@example.com"
    # first signup
    r1 = app_client.post("/activities/Gym%20Class/signup", params={"email": email})
    assert r1.status_code == 200
    # second signup should fail with 409
    r2 = app_client.post("/activities/Gym%20Class/signup", params={"email": email})
    assert r2.status_code == 409


def test_signup_full(app_client):
    activity = "Debate Team"
    from src.app import activities as activities_ref
    # fill participants to capacity
    activities_ref[activity]["participants"] = [f"u{i}@example.com" for i in range(activities_ref[activity]["max_participants"])]
    res = app_client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": "extra@example.com"})
    assert res.status_code == 400


def test_remove_participant_success(app_client):
    activity = "Chess Club"
    email = "removeme@example.com"
    # ensure present via signup
    app_client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    del_res = app_client.delete(f"/activities/{urllib.parse.quote(activity)}/participants/{urllib.parse.quote(email)}")
    assert del_res.status_code == 200
    data = app_client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_remove_participant_not_found(app_client):
    activity = "Chess Club"
    email = "notfound@example.com"
    del_res = app_client.delete(f"/activities/{urllib.parse.quote(activity)}/participants/{urllib.parse.quote(email)}")
    assert del_res.status_code == 404
