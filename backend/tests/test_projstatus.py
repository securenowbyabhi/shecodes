import requests

BASE_URL = "http://127.0.0.1:8000/shecodes"

def test_project_status():
    params = {"projectid": "P123456"}
    r = requests.get(f"{BASE_URL}/projectstatus", params=params)

    assert r.status_code in [200, 404]
    data = r.json()
    assert "message" in data
