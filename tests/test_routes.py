# tests/test_routes.py
import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """Create app fixture for tests."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """Create test client fixture."""
    return app.test_client()


def test_home_route(client):
    """Test that home route returns successful response."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Word Train Game' in response.data


def test_favicon_route(client):
    """Test that favicon route returns correct response."""
    response = client.get('/favicon.ico')
    assert response.status_code in (200, 302, 304)  # Different valid responses
