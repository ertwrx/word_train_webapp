import requests
import logging
from typing import Dict, Any, Optional
import functools
import time
from flask import current_app

# Setup logger
logger = logging.getLogger(__name__)

# Simple in-memory cache
_definition_cache = {}
_cache_timeout = 86400  # 24 hours in seconds

def get_definition(word: str) -> str:
    """
    Gets definition for a word from dictionary API or special cases.
    
    Args:
        word (str): The word to get definition for
        
    Returns:
        str: HTML formatted definition string
    """
    if not word:
        return "Enter a word to see its definition!"
    
    # Check cache first
    cache_key = word.lower().strip()
    if cache_key in _definition_cache:
        cache_entry = _definition_cache[cache_key]
        if time.time() - cache_entry['timestamp'] < _cache_timeout:
            logger.debug(f"Cache hit for '{word}'")
            return cache_entry['definition']
    
    # Special case checks
    lowerword = word.lower().replace(/\s+/g, '')
    
    # Special case for Erwin
    if lowerword == "erwin":
        definition = '<span style="font-style: italic; font-weight: bold; color: #9b59b6; font-size: 1.2em; font-family: \'Arial\', sans-serif;">This guy\'s idea was so good, even ChatGPT had to sit down and take notes. 📝🤖🔥</span>'
        _cache_definition(cache_key, definition)
        return definition
    
    # Special case for Jesus/Christ
    if "jesus" in lowerword or "christ" in lowerword:
        definition = '<span style="font-style: italic; font-weight: bold; color: #e74c3c; font-size: 1.2em; font-family: \'Georgia\', serif;">My Lord, My God, My Savior!! All Glory to God in the highest!!! 🙌</span>'
        _cache_definition(cache_key, definition)
        return definition
    
    try:
        # Clean the word for API call
        clean_word = word.split()[0].lower()
        clean_word = ''.join(c for c in clean_word if c.isalpha())
        
        if not clean_word:
            return "Maybe try entering... you know... actual letters? 😉"
            
        # Make API request
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{clean_word}", timeout=3)
        
        # Handle word not found
        if not response.ok:
            logger.warning(f"Dictionary API returned non-OK status ({response.status}) for '{clean_word}'")
            word_not_found_responses = [
                f'"{word}"? I looked everywhere but couldn\'t find this word! 🕵️‍♂️',
                f'Ah! Do you speak the language of the ancients? "{word}" is a mystery to me! 🧙‍♂️',
                f'Hmm, "{word}" sounds made up. But then again, aren\'t all words? 🤔',
                f'I tried asking my dictionary friends about "{word}", but they just laughed! 📚',
                f'"{word}" - Is that from a sci-fi novel or did you just sneeze? 🤧',
                f'My dictionary threw a 404 error page at me for "{word}". Rude! 📄',
                f'Is "{word}" even legal in Scrabble? Doesn\'t look like it\'s in my dictionary!'
            ]
            import random
            definition = random.choice(word_not_found_responses)
            _cache_definition(cache_key, definition)
            return definition
        
        # Process successful response
        data = response.json()
        meanings = data[0].get('meanings', []) if data else []
        
        if meanings and meanings[0].get('definitions') and meanings[0]['definitions']:
            part_of_speech = meanings[0].get('partOfSpeech', 'unknown')
            definition_text = meanings[0]['definitions'][0]['definition']
            definition = f'<strong>{clean_word}</strong> <em>({part_of_speech})</em>: {definition_text}'
            _cache_definition(cache_key, definition)
            return definition
        else:
            weird_data_responses = [
                f'Found "{clean_word}" but the definition seems to have wandered off... 🚶‍♂️',
                f'The entry for "{clean_word}" exists, but it\'s written in invisible ink! ✨',
                f'"{clean_word}" is in the dictionary, but the definition is playing hide-and-seek! 🙈'
            ]
            definition = random.choice(weird_data_responses)
            _cache_definition(cache_key, definition)
            return definition
            
    except Exception as e:
        logger.error(f"Error fetching definition for '{word}': {str(e)}")
        connection_error_responses = [
            f'Is the dictionary API napping? 😴 Couldn\'t get a definition for "{word}".',
            f'My wires must be crossed! ⚡️ Failed to look up "{word}". Try again?',
            f'The definition gnomes are on strike! ✊ Couldn\'t fetch "{word}".',
            f'Uh oh, hit some turbulence trying to fetch "{word}". ✈️ Maybe try again later?',
            f'The dictionary server might be lost in translation... 🌐 Error fetching "{word}".',
            f'Whoops! Dropped the dictionary while looking up "{word}". 📚 Try again!',
            f'Static electricity? Gremlins? 👾 Couldn\'t connect to fetch "{word}".',
            f'Does the internet exist right now? 🤔 Couldn\'t reach the dictionary for "{word}".'
        ]
        definition = random.choice(connection_error_responses)
        # Don't cache errors
        return definition

def _cache_definition(key: str, definition: str) -> None:
    """Store definition in cache with current timestamp"""
    _definition_cache[key] = {
        'definition': definition,
        'timestamp': time.time()
    }
    
    # Limit cache size to prevent memory issues
    if len(_definition_cache) > 1000:  # Arbitrary limit
        # Remove oldest 20% of entries
        items = sorted(_definition_cache.items(), key=lambda x: x[1]['timestamp'])
        for i in range(int(len(items) * 0.2)):
            if items[i][0] in _definition_cache:
                del _definition_cache[items[i][0]]

# Function to generate random words - could be moved from client side
def generate_random_word() -> str:
    """Generate a random word from API or fallback to local list"""
    try:
        response = requests.get('https://random-word-api.vercel.app/api?words=1', timeout=3)
        if response.ok:
            data = response.json()
            if data and data[0]:
                return data[0]
        raise Exception("API call failed or returned invalid data")
    except Exception as e:
        logger.warning(f"Random word API error: {str(e)}")
        fallback_words = [
            "You are enough", "You can do it", "Stay in peace", "Feel the joy", 
            "Keep your hope", "Trust your path", "Love is here", "Dream without fear", 
            "Shine your light", "Make it happen", "You are valued", "Keep moving forward", 
            "Stay strong now", "Be truly brave", "Embrace the calm"
        ]
        import random
        return random.choice(fallback_words)
