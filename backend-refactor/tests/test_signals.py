"""Tests for Signal endpoints."""

from fastapi.testclient import TestClient


def test_create_signal(client: TestClient, base_asset):
    payload = {
        "signal_id": "TEST-SIGNAL-001",
        "signal_name": "Voltage Reading",
        "unit": "kV",
        "asset_id": str(base_asset.id),
    }
    response = client.post("/api/signals", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["signal_id"] == "TEST-SIGNAL-001"
    assert data["signal_name"] == "Voltage Reading"
    assert data["unit"] == "kV"


def test_create_signal_duplicate_signal_id(client: TestClient, base_asset):
    payload = {
        "signal_id": "DUPLICATE-SIGNAL",
        "signal_name": "Test",
        "unit": "V",
        "asset_id": str(base_asset.id),
    }
    response1 = client.post("/api/signals", json=payload)
    assert response1.status_code == 201

    response2 = client.post("/api/signals", json=payload)
    assert response2.status_code == 409
    assert "already exists" in response2.json()["detail"]


def test_list_signals(client: TestClient, base_asset):
    for i in range(3):
        payload = {
            "signal_id": f"SIGNAL-{i:03d}",
            "signal_name": f"Signal {i}",
            "unit": "V",
            "asset_id": str(base_asset.id),
        }
        client.post("/api/signals", json=payload)

    response = client.get("/api/signals?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2


def test_get_signal_by_id(client: TestClient, base_signal):
    response = client.get(f"/api/signals/{base_signal.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(base_signal.id)
    assert data["signal_id"] == "BASE-SIGNAL-001"


def test_get_signal_not_found(client: TestClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/signals/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_signal(client: TestClient, base_signal):
    payload = {
        "signal_id": "UPDATED-SIGNAL",
        "signal_name": "Updated Signal Name",
        "unit": "mV",
    }
    response = client.put(f"/api/signals/{base_signal.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["signal_id"] == "UPDATED-SIGNAL"
    assert data["signal_name"] == "Updated Signal Name"
    assert data["unit"] == "mV"


def test_delete_signal(client: TestClient, base_asset):
    payload = {
        "signal_id": "DELETE-SIGNAL",
        "signal_name": "To Delete",
        "unit": "V",
        "asset_id": str(base_asset.id),
    }
    res_create = client.post("/api/signals", json=payload)
    data = res_create.json()
    signal_id = data["id"]

    response = client.delete(f"/api/signals/{signal_id}")
    assert response.status_code == 204

    response = client.get(f"/api/signals/{signal_id}")
    assert response.status_code == 404


def test_get_signals_by_asset(client: TestClient, base_asset):
    for i in range(2):
        payload = {
            "signal_id": f"ASSET-SIGNAL-{i}",
            "signal_name": f"Asset Signal {i}",
            "unit": "V",
            "asset_id": str(base_asset.id),
        }
        client.post("/api/signals", json=payload)

    response = client.get(f"/api/assets/{base_asset.id}/signals")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 2
