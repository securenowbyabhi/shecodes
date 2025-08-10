import requests

BASE_URL = "http://127.0.0.1:8000/shecodes"

def test_login():
    payload = {
        "username": "testuser123",
        "password": "securepass"
    }
    r = requests.post(f"{BASE_URL}/login", json=payload)

    assert r.status_code in [200, 401]
    data = r.json()
    assert "message" in data
