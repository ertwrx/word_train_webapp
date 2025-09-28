import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from flask import Flask, request, render_template, session, jsonify
import random
import logging
from config import config
import click
from app.dictionary_service import get_definition, generate_random_word
from app.api_routes import api  # Corrected import path

# Initialize Flask application
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static"),
)
config.apply_config(app)

# Register the blueprint after the app is created
app.register_blueprint(api)

# Setup logger for this module
logger = logging.getLogger(__name__)




@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    message = ""
    speed = 12
    engine = "🚂"  # Set a default engine for GET requests
    initial_definition = ""

    if request.method == "GET" or "challenge_word" not in session:
        session["challenge_word"] = random.choice(
            ["python", "emoji", "rocket", "train", "erwin"]
        )

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
            output = [user_word]

            session.setdefault("history", [])
            session["history"].append(user_word)

            if user_word.lower().strip() == challenge_word.lower():
                message = "Nice! You matched the challenge! 🎉"
                logger.info(f"Match successful for user word: {user_word}")
            else:
                message = "Try again! 🎯"
                logger.info(f"Match failed for user word: {user_word}")

            new_challenge = random.choice(
                ["python", "emoji", "rocket", "train", "erwin"]
            )
            while new_challenge.lower() == challenge_word.lower():
                new_challenge = random.choice(
                    ["python", "emoji", "rocket", "train", "erwin"]
                )
            session["challenge_word"] = new_challenge
            challenge_word = new_challenge

            # Get initial definition for the word (server-side)
            initial_definition = get_definition(user_word)
        else:
            message = "Please enter a word!"
            logger.warning("Empty word submission received")

    # If it's an AJAX request specifically for definitions
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.args.get('get_definition'):
        word = request.args.get('word', '')
        return jsonify({'definition': get_definition(word)})

    # If it's an AJAX request for random words
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.args.get('random_word'):
        return jsonify({'word': generate_random_word()})

    return render_template(
        "index.html",
        output=output,
        message=message,
        challenge_word=challenge_word,
        speed=speed,
        engine=engine,
        initial_definition=initial_definition
    )


# CLI commands for admin tasks
@app.cli.command("clear-sessions")
def clear_sessions_command():
    """Clear all session data."""
    session.clear()
    logger.info("All sessions cleared")
    click.echo("All sessions have been cleared.")


@app.cli.command("list-words")
def list_words_command():
    """List all challenge words available."""
    words = ["python", "emoji", "rocket", "train", "erwin"]
    click.echo("Available challenge words:")
    for word in words:
        click.echo(f"- {word}")


# Add routes for API endpoints
@app.route("/api/define/<word>", methods=["GET"])
def define_word_api(word):
    """API endpoint to get a word definition"""
    definition = get_definition(word)
    return jsonify({"word": word, "definition": definition})


@app.route("/api/random-word", methods=["GET"])
def random_word_api():
    """API endpoint to get a random word"""
    word = generate_random_word()
    return jsonify({"word": word})


if __name__ == "__main__":
    app.run(debug=config.DEBUG, host=config.HOST)
