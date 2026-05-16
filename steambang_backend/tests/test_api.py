"""API integration tests for (S)TeemBang."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed import ADMIN_EMAIL, ADMIN_PASSWORD, DEMO_EMAIL, DEMO_PASSWORD


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_register_login_dashboard(client: TestClient) -> None:
    email = "pytest_member@example.com"
    password = "secret12"

    r = client.post(
        "/api/auth/register",
        json={"name": "Pytest Runner", "email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["role"] == "member"

    r = client.post(
        "/api/activities",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "activity_type": "workout",
            "category": "running",
            "title": "Morning run",
            "duration_minutes": 30,
        },
    )
    assert r.status_code == 201, r.text
    assert r.json()["calories_burned"] > 0

    r = client.post(
        "/api/activities/steps/sync",
        headers={"Authorization": f"Bearer {token}"},
        json={"steps": 4500},
    )
    assert r.status_code == 200
    assert r.json()["steps"] == 4500

    r = client.post(
        "/api/goals",
        headers={"Authorization": f"Bearer {token}"},
        json={"metric": "steps", "period": "daily", "target_value": 8000},
    )
    assert r.status_code == 201

    r = client.get("/api/analytics/dashboard", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    dash = r.json()
    assert dash["today_steps"] >= 4500
    assert dash["today_workouts"] >= 1


def test_demo_user_seeded(client: TestClient) -> None:
    r = client.post("/api/auth/login", json={"email": DEMO_EMAIL, "password": DEMO_PASSWORD})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get("/api/analytics/trends?days=7", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert len(r.json()["points"]) == 7


def test_admin_stats(client: TestClient) -> None:
    r = client.post("/api/auth/login", json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200
    token = r.json()["access_token"]

    r = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    stats = r.json()
    assert stats["total_users"] >= 2

    r = client.get("/api/admin/stats")
    assert r.status_code == 401
