# Created by: ertwrx
# Created at: 2025-04-18 14:25:00 UTC

import random
from typing import Dict, Any

def generate_word_train(word: str, engine: str = "🚂") -> str:
    """
    Generates a graphical word train representation with spinning SVG wheels.
    
    Args:
        word (str): The word to transform into a train
        engine (str): The engine emoji to use (default: "🚂")
    
    Returns:
        str: HTML string representing the word train
    """
    wheel_svg = """
    <svg class='wheel' viewBox='0 0 100 100'>
      <circle cx='50' cy='50' r='48' stroke='#333' stroke-width='4' fill='none'/>
      <line x1='50' y1='0' x2='50' y2='100' stroke='#555' stroke-width='4'/>
      <line x1='0' y1='50' x2='100' y2='50' stroke='#555' stroke-width='4'/>
      <line x1='15' y1='15' x2='85' y2='85' stroke='#777' stroke-width='3'/>
      <line x1='15' y1='85' x2='85' y2='15' stroke='#777' stroke-width='3'/>
    </svg>
    """

    train = engine
    for i, char in enumerate(word):
        style = ""
        if i == 0:
            style = f"<span style='font-size: 1.5em; font-weight: bold;'>[{char.upper()}]</span>"
        elif random.random() < 0.3:
            style = f"<span style='font-size: 1.2em;'>[{char.upper()}]</span>"
        elif random.random() < 0.6:
            style = f"<span style='font-size: 0.8em;'>-{char.lower()}-</span>"
        else:
            style = f"[{char.upper()}]"
        train += style + wheel_svg
    return train
