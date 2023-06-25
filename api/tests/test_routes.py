from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    temp = response.json()
    assert "foi_requests" in temp


def test_root_public_bodies():
    response = client.get("?category=public_body_id&selection=69")
    assert response.status_code == 200
    temp = response.json()
    assert "foi_requests" in temp


def test_root_jurisdictions():
    response = client.get("?category=jurisdiction_id&selection=1")
    assert response.status_code == 200
    temp = response.json()
    assert "foi_requests" in temp


def test_root_campaigns():
    response = client.get("?category=campaign_id&selection=13")
    assert response.status_code == 200
    temp = response.json()
    assert "foi_requests" in temp


def test_general_info():
    response = client.get("/general_info")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)


def test_ranking_campaigns():
    response = client.get("/ranking?typ=campaigns")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)
    response = client.get("/ranking?typ=campaigns&ascending=True&s=Anzahl")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)


def test_ranking_jurisdictions():
    response = client.get("/ranking?typ=jurisdictions")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)
    response = client.get("/ranking?typ=public_bodies&ascending=True&s=Anzahl")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)


def test_ranking_public_bodies():
    response = client.get("/ranking?typ=public_bodies")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)
    response = client.get("/ranking?typ=public_bodies&ascending=True&s=Anzahl")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)


def test_campaign_starts():
    response = client.get("/campaign_starts")
    assert response.status_code == 200
    temp = response.json()
    assert isinstance(temp, dict)
