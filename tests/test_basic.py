# tests/test_basic.py

def test_app_imports():
    """Verify the application can be imported without errors."""
    try:
        import app
        assert True
    except ImportError:
        assert False, "Failed to import the app module"


def test_flask_app_creation():
    """Test that Flask app can be created."""
    try:
        from app import create_app
        flask_app = create_app()
        assert flask_app is not None
    except (ImportError, AttributeError) as e:
        assert False, f"Failed to create Flask app: {e}"
