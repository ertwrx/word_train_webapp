# tests/test_game_logic.py
import pytest
from app.utils import validate_word, get_last_letter

# Adjust these function names and imports based on your actual implementation


def test_validate_word():
    """Test the word validation function."""
    # Simple test for word validation
    assert validate_word("hello") is True
    assert validate_word("") is False
    assert validate_word("123") is False
    

def test_get_last_letter():
    """Test getting the last letter from a word."""
    assert get_last_letter("hello") == "o"
    assert get_last_letter("test") == "t"
    assert get_last_letter("") is None
