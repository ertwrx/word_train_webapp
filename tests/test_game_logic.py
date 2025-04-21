# tests/test_game_logic.py
from app import check_word_valid, get_next_letter


def test_check_word_valid():
    """Test the word validation function."""
    # Test with valid English words
    assert check_word_valid('cat') is True
    assert check_word_valid('dog') is True
    assert check_word_valid('house') is True
    
    # Test with invalid inputs
    assert check_word_valid('') is False  # Empty string
    assert check_word_valid('xyz123') is False  # Non-word
    assert check_word_valid('notarealwordxxxyyy') is False  # Made-up word
    

def test_get_next_letter():
    """Test the function that gets the next required letter."""
    assert get_next_letter('cat') == 't'
    assert get_next_letter('dog') == 'g'
    assert get_next_letter('house') == 'e'
    assert get_next_letter('') is None  # Empty string edge case
