# tests/test_socketio.py
import pytest
from flask_socketio import SocketIOTestClient
from app import app, socketio


@pytest.fixture
def socketio_client():
    """Create a SocketIO test client."""
    flask_app = app
    flask_app.config['TESTING'] = True
    return SocketIOTestClient(flask_app, socketio)


def test_socketio_connection(socketio_client):
    """Test that a client can connect to SocketIO."""
    assert socketio_client.is_connected()


def test_join_event(socketio_client):
    """Test the join event."""
    socketio_client.emit('join', {'username': 'testuser', 'room': 'global'})
    received = socketio_client.get_received()
    assert len(received) > 0
    
    # Find a response that includes the user joining
    join_events = [event for event in received if event['name'] == 'status' 
                  and isinstance(event['args'], list) 
                  and len(event['args']) > 0 
                  and 'testuser' in str(event['args'][0])]
    
    assert len(join_events) > 0, "Join event not properly handled"


def test_submit_word_event(socketio_client):
    """Test the submit word event."""
    # First join a room
    socketio_client.emit('join', {'username': 'testuser', 'room': 'global'})
    socketio_client.get_received()  # Clear received messages
    
    # Submit a word
    socketio_client.emit('submit_word', {'word': 'cat', 'room': 'global'})
    received = socketio_client.get_received()
    
    # Check for appropriate response events
    word_events = [event for event in received if event['name'] == 'new_word' 
                  and isinstance(event['args'], list) 
                  and len(event['args']) > 0]
    
    assert len(word_events) > 0, "Word submission not properly handled"
