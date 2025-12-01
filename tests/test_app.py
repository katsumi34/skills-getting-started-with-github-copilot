import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # 新規メールでサインアップ
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # まず削除（存在しない場合は無視）
    client.delete(f"/activities/{activity}/unregister", params={"email": email})
    # サインアップ
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # もう一度サインアップはエラー
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # 削除
    response3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response3.status_code == 200
    assert f"Removed {email}" in response3.json()["message"]
    # もう一度削除はエラー
    response4 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert response4.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/UnknownActivity/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
