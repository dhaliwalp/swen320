import pytest
from app.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home Page' in response.data

def test_register(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data