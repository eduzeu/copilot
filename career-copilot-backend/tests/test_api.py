def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_user_routes_require_authentication(client):
    assert client.get("/users/me").status_code == 401
    assert client.delete("/users/me").status_code == 401


def test_application_crud_is_reflected_in_dashboard(client, auth_headers):
    created = client.post(
        "/applications/",
        headers=auth_headers,
        json={
            "company": "Example",
            "role_title": "Engineer",
            "location": "Remote",
            "date_applied": "2026-07-12",
            "status": "interview",
        },
    )
    assert created.status_code == 200, created.text
    assert created.json()["location"] == "Remote"

    dashboard = client.get("/dashboard/", headers=auth_headers)
    assert dashboard.status_code == 200
    assert dashboard.json()["total_applications"] == 1
    assert dashboard.json()["interviewing"] == 1

    deleted = client.delete(f"/applications/{created.json()['id']}", headers=auth_headers)
    assert deleted.status_code == 204


def test_ai_routes_require_authentication(client):
    assert client.post("/analysis/score", params={"resume_text": "x", "job_description": "y"}).status_code == 401
