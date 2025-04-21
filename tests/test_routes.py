# tests/test_routes.py
import pytest
from app import create_app


@pytest.fixture
def app():
    """Create app fixture for tests."""
    flask_app = create_app()
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
    # Adjust the content check based on what's actually in your HTML
    assert b'<!DOCTYPE html>' in response.data


def test_favicon_route(client):
    """Test that favicon route returns some response."""
    response = client.get('/favicon.ico')
    # Just check that it doesn't 500 error
    assert response.status_code != 500
