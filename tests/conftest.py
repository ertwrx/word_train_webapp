# tests/conftest.py
# This file contains pytest fixtures that can be shared across multiple test files

import pytest
from app import app as flask_app


@pytest.fixture(scope="session")
def app():
    """Create app fixture for tests."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture(scope="session")
def client(app):
    """Create test client fixture."""
    return app.test_client()
