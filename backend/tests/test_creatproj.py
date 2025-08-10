import requests

BASE_URL = "http://127.0.0.1:8000/shecodes"

def test_create_project():
    payload = {
        "projectid": "P123456",
        "projectname": "AI Chatbot",
        "description": "A chatbot using GPT models"
    }
    r = requests.post(f"{BASE_URL}/createproject", json=payload)

    assert r.status_code in [200, 400]
    data = r.json()
    assert "message" in data


def test_create_project_already_exists():
    # mock db as a dict
    mock_db_projects = {
        "Projects": {
            "projectid": "1444",
            "projectname": "Existing Project",
            "description": "Already exists",
            "phardware": [0,0]
        }
    }

    payload = {
        "projectid": "1444",
        "projectname": "Existing Project",
        "description": "Already exists",
        
    }  
    r = requests.post(f"{BASE_URL}/createproject", json=payload)
    assert r.status_code in [200, 400]
    data = r.json()
    assert "Project Id already exists" in data.get("message", "")