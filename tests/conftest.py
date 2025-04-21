# tests/conftest.py
# This file contains pytest fixtures that can be shared across multiple test files

import pytest
from app import create_app  # Assuming there's a create_app function


@pytest.fixture(scope="session")
def app():
    """Create app fixture for tests."""
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture(scope="session")
def client(app):
    """Create test client fixture."""
    return app.test_client()
