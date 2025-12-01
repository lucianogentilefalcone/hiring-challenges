"""Tests for Measurement endpoints."""

from fastapi.testclient import TestClient
from datetime import datetime, timedelta


def test_create_measurement(client: TestClient, base_signal):
    now = datetime.utcnow()
    payload = {
        "value": 115.5,
        "timestamp": now.isoformat(),
        "signal_id": str(base_signal.id),
    }
    response = client.post("/api/measurements", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 115.5
    assert "id" in data
    assert "timestamp" in data


def test_list_measurements(client: TestClient, base_signal):
    now = datetime.utcnow()
    for i in range(3):
        payload = {
            "value": 100.0 + i,
            "timestamp": (now - timedelta(hours=i)).isoformat(),
            "signal_id": str(base_signal.id),
        }
        client.post("/api/measurements", json=payload)

    response = client.get("/api/measurements?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 3
    assert len(data["items"]) == 2


def test_get_measurement_by_id(client: TestClient, base_signal):
    now = datetime.utcnow()
    payload = {
        "value": 120.0,
        "timestamp": now.isoformat(),
        "signal_id": str(base_signal.id),
    }
    res_create = client.post("/api/measurements", json=payload)
    measurement_id = res_create.json()["id"]

    response = client.get(f"/api/measurements/{measurement_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == measurement_id
    assert data["value"] == 120.0


def test_get_measurement_not_found(client: TestClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/measurements/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_measurement(client: TestClient, base_signal):
    now = datetime.utcnow()
    payload = {
        "value": 100.0,
        "timestamp": now.isoformat(),
        "signal_id": str(base_signal.id),
    }
    res_create = client.post("/api/measurements", json=payload)
    measurement_id = res_create.json()["id"]

    update_payload = {
        "value": 150.0,
        "timestamp": (now + timedelta(hours=1)).isoformat(),
    }
    response = client.put(f"/api/measurements/{measurement_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 150.0


def test_delete_measurement(client: TestClient, base_signal):
    now = datetime.utcnow()
    payload = {
        "value": 100.0,
        "timestamp": now.isoformat(),
        "signal_id": str(base_signal.id),
    }
    res_create = client.post("/api/measurements", json=payload)
    measurement_id = res_create.json()["id"]

    response = client.delete(f"/api/measurements/{measurement_id}")
    assert response.status_code == 204

    response = client.get(f"/api/measurements/{measurement_id}")
    assert response.status_code == 404


def test_get_signal_statistics(client: TestClient, base_signal):
    now = datetime.utcnow()
    values = [100.0, 120.0, 110.0, 130.0, 105.0]
    for i, value in enumerate(values):
        payload = {
            "value": value,
            "timestamp": (now - timedelta(hours=i)).isoformat(),
            "signal_id": str(base_signal.id),
        }
        client.post("/api/measurements", json=payload)

    from_date = (now - timedelta(hours=5)).isoformat()
    to_date = now.isoformat()
    response = client.get(
        f"/api/measurements/signal/{base_signal.id}/stats"
        f"?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 5
    assert data["mean"] == 113.0
    assert data["min"] == 100.0
    assert data["max"] == 130.0
    assert "median" in data
    assert "std_dev" in data
