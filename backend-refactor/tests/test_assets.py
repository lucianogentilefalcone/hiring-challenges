"""Tests for Asset endpoints."""

from fastapi.testclient import TestClient


def test_create_asset(client: TestClient):
    payload = {
        "asset_id": "TEST-ASSET-001",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Test asset in NYC",
    }
    response = client.post("/api/assets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["asset_id"] == "TEST-ASSET-001"
    assert data["latitude"] == 40.7128
    assert data["longitude"] == -74.0060
    assert "id" in data


def test_create_asset_duplicate_asset_id(client: TestClient):
    payload = {
        "asset_id": "DUPLICATE-001",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Test",
    }
    response1 = client.post("/api/assets", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/assets", json=payload)
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"]


def test_list_assets(client: TestClient):
    for i in range(3):
        payload = {
            "asset_id": f"ASSET-{i:03d}",
            "latitude": 40.0 + i,
            "longitude": -74.0 + i,
            "description": f"Asset {i}",
        }
        client.post("/api/assets", json=payload)

    response = client.get("/api/assets?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2


def test_list_assets_default_pagination(client: TestClient):
    payload = {
        "asset_id": "DEFAULT-PAGINATION-TEST",
        "latitude": 40.0,
        "longitude": -74.0,
        "description": "Test",
    }
    client.post("/api/assets", json=payload)

    response = client.get("/api/assets")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_asset_by_id(client: TestClient, base_asset):
    response = client.get(f"/api/assets/{base_asset.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(base_asset.id)
    assert data["asset_id"] == "BASE-ASSET-001"


def test_get_asset_not_found(client: TestClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/assets/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_asset(client: TestClient, base_asset):
    payload = {
        "asset_id": "UPDATED-001",
        "latitude": 41.0000,
        "longitude": -75.0000,
        "description": "Updated asset",
    }
    response = client.put(f"/api/assets/{base_asset.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == "UPDATED-001"
    assert data["latitude"] == 41.0000


def test_delete_asset(client: TestClient):
    payload = {
        "asset_id": "DELETE-ME-001",
        "latitude": 40.0,
        "longitude": -74.0,
        "description": "To delete",
    }
    res_create = client.post("/api/assets", json=payload)
    asset_id = res_create.json()["id"]

    response = client.delete(f"/api/assets/{asset_id}")
    assert response.status_code == 204

    response = client.get(f"/api/assets/{asset_id}")
    assert response.status_code == 404
