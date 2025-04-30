import os
import sys
import pytest

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from first import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    """Test if login page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_signup_page(client):
    """Test if signup page loads successfully"""
    response = client.get('/signup')
    assert response.status_code == 200

def test_about_page(client):
    """Test if about page loads successfully"""
    response = client.get('/about')
    assert response.status_code == 200

def test_invalid_route(client):
    """Test if 404 page is returned for invalid routes"""
    response = client.get('/invalid-route')
    assert response.status_code == 404 