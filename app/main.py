import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from flask import Flask, request, render_template, session
import random
import logging
from config import config
import click


# Initialize Flask application
app = Flask(__name__,
           template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
           static_folder=os.path.join(os.path.dirname(__file__), 'static'))
config.apply_config(app)


# Setup logger for this module
logger = logging.getLogger(__name__)

def generate_word_train(word, engine="🚂"):
    """Generates a graphical word train representation with spinning SVG wheels."""
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

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    message = ""
    speed = 12

    if request.method == "GET" or "challenge_word" not in session:
        session["challenge_word"] = random.choice(["python", "emoji", "rocket", "train", "erwin"])
    
    challenge_word = session["challenge_word"]

    if request.method == "POST":
        # Get and clean user input
        user_word = request.form.get("word", "").strip()
        
        # Debug logging (replacing print statements)
        logger.debug("=== Debug Information ===")
        logger.debug(f"Raw form data: {dict(request.form)}")
        logger.debug(f"User word (raw): '{request.form.get('word', '')}'")
        logger.debug(f"User word (stripped): '{user_word}'")
        logger.debug(f"Challenge word (from session): '{challenge_word}'")

        engine = request.form.get("engine", "🚂")
        speed = int(request.form.get("speed", 12))

        if user_word:
            output = [engine + user_word]
            
            session.setdefault("history", [])
            session["history"].append(user_word)

            if user_word.lower().strip() == challenge_word.lower():
                message = "Nice! You matched the challenge! 🎉"
                logger.info(f"Match successful for user word: {user_word}")
            else:
                message = "Try again! 🎯"
                logger.info(f"Match failed for user word: {user_word}")
            
            new_challenge = random.choice(["python", "emoji", "rocket", "train", "erwin"])
            while new_challenge.lower() == challenge_word.lower():
                new_challenge = random.choice(["python", "emoji", "rocket", "train", "erwin"])
            session["challenge_word"] = new_challenge
            challenge_word = new_challenge
        else:
            message = "Please enter a word!"
            logger.warning("Empty word submission received")

    return render_template(
        "index.html",
        output=output,
        message=message,
        challenge_word=challenge_word,
        speed=speed
    )

# CLI commands for admin tasks
@app.cli.command("clear-sessions")
def clear_sessions_command():
    """Clear all session data."""
    session.clear()
    logger.info("All sessions cleared")
    click.echo('All sessions have been cleared.')

@app.cli.command("list-words")
def list_words_command():
    """List all challenge words available."""
    words = ["python", "emoji", "rocket", "train", "erwin"]
    click.echo('Available challenge words:')
    for word in words:
        click.echo(f"- {word}")

if __name__ == "__main__":
    app.run(
        debug=config.DEBUG,
        host=config.HOST
    )
