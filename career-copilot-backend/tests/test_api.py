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
    assert client.post("/coach/chat", json={"message": "Plan my week"}).status_code == 401


def test_career_profile_can_be_created_and_updated(client, auth_headers):
    initial = client.get("/profile/", headers=auth_headers)
    assert initial.status_code == 200
    assert initial.json()["status"] == "college"

    payload = initial.json()
    for generated in ("id", "user_id", "created_at", "updated_at", "completeness"):
        payload.pop(generated)
    payload.update({
        "status": "college",
        "school": "Example University",
        "major": "Computer Science",
        "graduation_year": 2027,
        "technical_skills": ["Python", "React"],
        "target_roles": ["Software Engineer"],
        "primary_goal": "Land a summer internship",
    })
    saved = client.put("/profile/", headers=auth_headers, json=payload)
    assert saved.status_code == 200, saved.text
    assert saved.json()["major"] == "Computer Science"
    assert saved.json()["completeness"] > initial.json()["completeness"]


def test_coach_chat_uses_profile_without_requiring_a_resume(client, auth_headers, monkeypatch):
    monkeypatch.setattr(
        "app.services.coach_service.call_llm",
        lambda *args, **kwargs: "Focus on two targeted applications and one DSA session.",
    )
    response = client.post(
        "/coach/chat",
        headers=auth_headers,
        json={"message": "Plan my week", "mode": "weekly_plan"},
    )
    assert response.status_code == 200, response.text
    assert response.json()["mode"] == "weekly_plan"
    assert response.json()["context_used"] == ["career profile"]
