def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/health/live").status_code == 200
    ready = client.get("/health/ready")
    assert ready.status_code == 200
    assert ready.json()["database"] == "up"


def test_cookie_login_and_logout(client):
    client.post("/auth/register", json={"email": "cookie@example.com", "password": "password123"})
    logged_in = client.post("/auth/login", json={"email": "cookie@example.com", "password": "password123"})
    assert logged_in.status_code == 200
    assert logged_in.cookies.get("career_copilot_session")
    assert client.get("/users/me").status_code == 200
    assert client.post("/auth/logout").status_code == 204
    assert client.get("/users/me").status_code == 401


def test_invalid_login_is_generic(client):
    response = client.post("/auth/login", json={"email": "missing@example.com", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


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


def test_users_cannot_access_each_others_applications(client):
    client.post("/auth/register", json={"email": "first@example.com", "password": "password123"})
    first_login = client.post("/auth/login", json={"email": "first@example.com", "password": "password123"})
    first = {"Authorization": f"Bearer {first_login.json()['access_token']}"}
    created = client.post(
        "/applications/",
        headers=first,
        json={"company": "Private", "role_title": "Engineer", "location": "NYC", "date_applied": "2026-07-21", "status": "applied"},
    ).json()

    client.post("/auth/register", json={"email": "second@example.com", "password": "password123"})
    second_login = client.post("/auth/login", json={"email": "second@example.com", "password": "password123"})
    second = {"Authorization": f"Bearer {second_login.json()['access_token']}"}
    assert client.get(f"/applications/{created['id']}", headers=second).status_code == 404
    assert client.delete(f"/applications/{created['id']}", headers=second).status_code == 404


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
    assert response.json()["strategy"] == "direct_action"
    assert response.json()["interaction_id"] > 0

    feedback = client.put(
        f"/coach/interactions/{response.json()['interaction_id']}/feedback",
        headers=auth_headers,
        json={"helpful": True},
    )
    assert feedback.status_code == 200, feedback.text
    assert feedback.json()["helpful"] is True


def test_coach_uses_offline_fallback_when_ai_key_is_missing(client, auth_headers, monkeypatch):
    from app.core.config import settings

    monkeypatch.setattr(settings, "ai_key", "")
    response = client.post(
        "/coach/chat",
        headers=auth_headers,
        json={"message": "Plan my week", "mode": "weekly_plan"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["fallback"] is True
    assert "AI_KEY is not configured" not in response.json()["answer"]
    assert "Best next move" in response.json()["answer"]


def test_non_resume_analysis_is_flagged_without_a_score(monkeypatch):
    from app.services.llm_analysis import analyze_resume_general

    monkeypatch.setattr(
        "app.services.llm_analysis.call_llm_json",
        lambda *args, **kwargs: {
            "is_resume": False,
            "quality_score": None,
            "feedback": "This is a financial aid letter, not a resume.",
            "rewrite_ats": None,
            "rewrite_strong": None,
            "suggestions": [],
            "quantification_suggestions": [],
        },
    )
    result = analyze_resume_general("financial aid letter contents")
    assert result["is_resume"] is False
    assert result["quality_score"] is None


def test_non_resume_job_match_has_no_zero_score(monkeypatch):
    from app.services.llm_analysis import score_resume_against_jd

    monkeypatch.setattr(
        "app.services.llm_analysis.call_llm_json",
        lambda *args, **kwargs: {
            "is_resume": False,
            "overall_score": None,
            "summary": "This is not a resume.",
            "strengths": [],
            "gaps": [],
            "missing_keywords": [],
            "recommendation": None,
        },
    )
    result = score_resume_against_jd("award letter", "software engineer role")
    assert result["is_resume"] is False
    assert result["overall_score"] is None
    assert result["recommendation"] is None


def test_ai_analysis_is_cached(client, auth_headers, monkeypatch):
    calls = {"count": 0}

    def fake_score(*args):
        calls["count"] += 1
        return {"is_resume": True, "overall_score": 80, "summary": "Good", "strengths": [], "gaps": [], "missing_keywords": [], "recommendation": "Good Match"}

    monkeypatch.setattr("app.api.routes.analysis.score_resume_against_jd", fake_score)
    params = {"resume_text": "A" * 60, "job_description": "B" * 60}
    first = client.post("/analysis/score", headers=auth_headers, params=params)
    second = client.post("/analysis/score", headers=auth_headers, params=params)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["cached"] is False
    assert second.json()["cached"] is True
    assert calls["count"] == 1


def test_weekly_plan_creates_trackable_actions(client, auth_headers, monkeypatch):
    monkeypatch.setattr(
        "app.services.coach_service.call_llm",
        lambda *args, **kwargs: "## Plan\n- Submit three targeted applications.\n- Complete two DSA sessions.\n\n## Best next move\nStart the first application.",
    )
    response = client.post(
        "/coach/chat",
        headers=auth_headers,
        json={"message": "Plan my week", "mode": "weekly_plan"},
    )
    assert response.status_code == 200, response.text
    actions = client.get("/coach/actions", headers=auth_headers).json()
    assert len(actions) == 2
    updated = client.put(
        f"/coach/actions/{actions[0]['id']}",
        headers=auth_headers,
        json={"status": "completed", "outcome": "Submitted and received a recruiter reply."},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "completed"
    assert "recruiter reply" in updated.json()["outcome"]


def test_coach_quota_error_returns_429(client, auth_headers, monkeypatch):
    from app.services.llm_service import LLMRateLimitError

    def quota_error(*args, **kwargs):
        raise LLMRateLimitError("Career Coach has reached today's Gemini free-tier limit.")

    monkeypatch.setattr("app.api.routes.coach.chat_with_career_coach", quota_error)
    response = client.post(
        "/coach/chat",
        headers=auth_headers,
        json={"message": "Help me plan my week"},
    )
    assert response.status_code == 429
    assert "free-tier limit" in response.json()["detail"]
