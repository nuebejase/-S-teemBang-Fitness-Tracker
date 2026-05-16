"""API integration tests (FastAPI TestClient, real SQLite file from conftest env)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.seed import ADMIN_EMAIL, ADMIN_PASSWORD


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_health(client: TestClient) -> None:
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_products_list_seeded(client: TestClient) -> None:
    r = client.get("/api/products")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 100
    assert all("id" in p and "name" in p and "price" in p for p in data)


def test_register_login_me_order_flow(client: TestClient) -> None:
    email = "pytest_customer@example.com"
    password = "secret12"

    r = client.post(
        "/api/auth/register",
        json={"name": "Pytest User", "email": email, "password": password},
    )
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]
    assert token

    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == email
    assert me["role"] == "customer"

    r = client.post(
        "/api/auth/register",
        json={"name": "Dup", "email": email, "password": password},
    )
    assert r.status_code == 400

    products = client.get("/api/products").json()
    pid = products[0]["id"]

    r = client.post(
        "/api/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [{"product_id": pid, "quantity": 1}],
            "customer_name": "Pytest User",
            "customer_email": email,
            "customer_phone": "09123456789",
            "address": "123 Test St, Metro Manila",
            "payment_method": "gcash",
            "delivery_fee": 50,
        },
    )
    assert r.status_code == 200, r.text
    order = r.json()
    assert order["id"].startswith("FS-")
    assert order["status"] == "pending"
    assert len(order["items"]) == 1
    assert order["items"][0]["quantity"] == 1
    assert order["total"] > 0

    r = client.get("/api/orders/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    mine = r.json()
    assert len(mine) >= 1
    assert mine[0]["id"] == order["id"]


def test_order_requires_customer_role(client: TestClient) -> None:
    r = client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert r.status_code == 200
    admin_token = r.json()["access_token"]

    products = client.get("/api/products").json()
    pid = products[0]["id"]

    r = client.post(
        "/api/orders",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "items": [{"product_id": pid, "quantity": 1}],
            "customer_name": "Admin",
            "customer_email": ADMIN_EMAIL,
            "customer_phone": "09",
            "address": "Addr",
            "payment_method": "cod",
            "delivery_fee": 50,
        },
    )
    assert r.status_code == 403


def test_order_requires_auth(client: TestClient) -> None:
    products = client.get("/api/products").json()
    pid = products[0]["id"]
    r = client.post(
        "/api/orders",
        json={
            "items": [{"product_id": pid, "quantity": 1}],
            "customer_name": "X",
            "customer_email": "x@y.com",
            "customer_phone": "09",
            "address": "A",
            "payment_method": "cod",
            "delivery_fee": 50,
        },
    )
    assert r.status_code == 401


def test_admin_product_crud_and_order_status(client: TestClient) -> None:
    r = client.post(
        "/api/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert r.status_code == 200
    admin_token = r.json()["access_token"]
    h = {"Authorization": f"Bearer {admin_token}"}

    r = client.post(
        "/api/products",
        headers=h,
        json={
            "name": "Pytest Scoop",
            "description": "Created by automated test",
            "price": 199.0,
            "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400",
            "category": "Special",
            "flavor": "Test",
            "stock": 5,
        },
    )
    assert r.status_code == 200, r.text
    created = r.json()
    pid = created["id"]
    assert created["name"] == "Pytest Scoop"

    r = client.patch(
        f"/api/products/{pid}",
        headers=h,
        json={"stock": 10, "price": 210.0},
    )
    assert r.status_code == 200
    assert r.json()["stock"] == 10
    assert float(r.json()["price"]) == 210.0

    # Customer places order for new product
    r = client.post(
        "/api/auth/register",
        json={"name": "Buyer", "email": "pytest_buyer2@example.com", "password": "secret12"},
    )
    assert r.status_code == 200
    cust_token = r.json()["access_token"]

    r = client.post(
        "/api/orders",
        headers={"Authorization": f"Bearer {cust_token}"},
        json={
            "items": [{"product_id": pid, "quantity": 2}],
            "customer_name": "Buyer",
            "customer_email": "pytest_buyer2@example.com",
            "customer_phone": "09999999999",
            "address": "456 Lane",
            "payment_method": "card",
            "delivery_fee": 50,
        },
    )
    assert r.status_code == 200, r.text
    oid = r.json()["id"]

    r = client.patch(
        f"/api/orders/{oid}/status",
        headers=h,
        json={"status": "processing"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "processing"

    r = client.delete(f"/api/products/{pid}", headers=h)
    assert r.status_code == 204


def test_login_invalid(client: TestClient) -> None:
    r = client.post(
        "/api/auth/login",
        json={"email": "nope@example.com", "password": "wrongpass"},
    )
    assert r.status_code == 401
