import requests

BASE_URL = "http://127.0.0.1:8000/shecodes"

def test_signup():
    payload = {
        "username": "testuser123",
        "password": "securepass"
    }
    r = requests.post(f"{BASE_URL}/signup", json=payload)

    assert r.status_code in [200, 201, 400]  # 400 if user exists
    data = r.json()
    assert "message" in data


def test_user_already_exists():
    # mock db as a dict
     mock_db_users = {
        "Users": {
            "username": "testuser123",
            "password": "securepass"
        }
    }

     payload = {
        "username": "testuser123",
        "password": "securepass"
        
    }  
     r = requests.post(f"{BASE_URL}/signup", json=payload)
     assert r.status_code in [200, 400]
     data = r.json()
     assert "Username already exists" in data.get("message", "")
