import requests

BASE_URL = "http://127.0.0.1:8000/shecodes"

def test_checkout():
    payload = {
        "projectid": "p101",
        "action": "checkout",
        "inventory": [
            {"hardwareid": "hw1", "quantity": 1}
        ]
    }
    r = requests.post(f"{BASE_URL}/checkincheckout", json=payload)

    assert r.status_code in [200, 400]
    data = r.json()
    assert "message" in data
