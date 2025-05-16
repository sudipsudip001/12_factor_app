from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app

client = TestClient(app)

def test_status():
    response = client.get("/working")
    assert response.status_code == 200
    assert response.json() == {"status": "yes working"}
