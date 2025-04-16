from flask import Flask, request, render_template, session
import random
import os  # Add this import

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

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
    challenge_word = random.choice(["python", "emoji", "rocket", "train", "erwin"])
    message = ""
    speed = 12

    if request.method == "POST":
        # Get and clean user input
        user_word = request.form.get("word", "").strip()
        
        # Debug prints
        print("\n=== Debug Information ===")
        print(f"Raw form data: {dict(request.form)}")
        print(f"User word (raw): '{request.form.get('word', '')}'")
        print(f"User word (stripped): '{user_word}'")
        print(f"Challenge word: '{challenge_word}'")
        print(f"Length of user word: {len(user_word)}")
        print(f"Length of challenge word: {len(challenge_word)}")
        print(f"ASCII values of user word: {[ord(c) for c in user_word]}")
        print(f"ASCII values of challenge word: {[ord(c) for c in challenge_word]}")
        print(f"User word bytes: {user_word.encode('utf-8')}")
        print(f"Challenge word bytes: {challenge_word.encode('utf-8')}")
        print("========================\n")

        engine = request.form.get("engine", "🚂")
        speed = int(request.form.get("speed", 12))

        if user_word:
            # Generate train visualization
            output = [generate_word_train(user_word, engine)]
            
            # Update session history
            session.setdefault("history", [])
            session["history"].append(user_word)

            # Normalize both strings for comparison
            normalized_user_word = user_word.lower().strip()
            normalized_challenge = challenge_word.lower().strip()
            
            print(f"Normalized user word: '{normalized_user_word}'")
            print(f"Normalized challenge: '{normalized_challenge}'")
            print(f"Do they match? {normalized_user_word == normalized_challenge}")

            if normalized_user_word == normalized_challenge:
                message = "Nice! You matched the challenge! 🎉"
                print("Match successful!")
            else:
                message = "Try again! 🎯"
                print("Match failed!")
        else:
            message = "Please enter a word!"
            print("No input received")

    return render_template(
        "index.html",
        output=output,
        message=message,
        challenge_word=challenge_word,
        speed=speed
    )

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    app.run(debug=debug_mode, host=host)
