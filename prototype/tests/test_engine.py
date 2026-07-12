import requests
import pytest

@pytest.fixture(autouse=True)
def reset_server_lattice():
    """
    Fixture to reset the server-side lattice before each test.
    """
    url = "http://localhost:8004/api/lattice/reset"
    try:
        requests.post(url, timeout=2)
    except requests.exceptions.ConnectionError:
        pass # If server is down, let the individual tests fail gracefully

def test_prototype_web_server_is_up():
    """
    Test that the Flask web server is up and serving on port 8004.
    """
    url = "http://localhost:8004/"
    try:
        response = requests.get(url, timeout=2)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail("The prototype web server is NOT running on port 8004!")

def test_api_geometry():
    url = "http://localhost:8004/api/geometry"
    response = requests.get(url, timeout=2)
    assert response.status_code == 200
    data = response.json()
    assert data["vertex_count"] == 24
    assert data["face_count"] == 14

def test_api_lattice_get():
    url = "http://localhost:8004/api/lattice"
    response = requests.get(url, timeout=2)
    assert response.status_code == 200
    data = response.json()
    # At least the root block should be present
    assert len(data) >= 1
    assert data[0]["coord"] == [0, 0, 0]
    assert data[0]["center"] == [0, 0, 0]
    assert data[0]["color"] == "red"

def test_api_lattice_place_block():
    url = "http://localhost:8004/api/lattice/place"
    payload = {
        "coord": [0, 0, 0],
        "face_direction": [1, 1, 1],
        "color": "blue"
    }
    response = requests.post(url, json=payload, timeout=2)
    assert response.status_code == 200
    data = response.json()
    
    # Check if the new block is in the list
    blue_block = None
    for b in data:
        if b["coord"] == [1, 1, 1]:
            blue_block = b
            break
            
    assert blue_block is not None
    assert blue_block["color"] == "blue"
    assert blue_block["center"] == [2, 2, 2]
