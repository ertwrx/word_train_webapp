from flask import Flask, request, render_template, session
import random
import os

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
    message = ""
    speed = 12

    # Generate new challenge word only on GET requests or if not in session
    if request.method == "GET" or "challenge_word" not in session:
        session["challenge_word"] = random.choice(["python", "emoji", "rocket", "train", "erwin"])
    
    challenge_word = session["challenge_word"]  # Get current challenge word

    if request.method == "POST":
        # Get and clean user input
        user_word = request.form.get("word", "").strip()
        
        # Debug prints
        print("\n=== Debug Information ===")
        print(f"Raw form data: {dict(request.form)}")
        print(f"User word (raw): '{request.form.get('word', '')}'")
        print(f"User word (stripped): '{user_word}'")
        print(f"Challenge word (from session): '{challenge_word}'")
        print("========================\n")

        engine = request.form.get("engine", "🚂")
        speed = int(request.form.get("speed", 12))

        if user_word:
            # Generate train visualization
            output = [generate_word_train(user_word, engine)]
            
            # Update session history
            session.setdefault("history", [])
            session["history"].append(user_word)

            # Compare the words
            if user_word.lower().strip() == challenge_word.lower():
                message = "Nice! You matched the challenge! 🎉"
                print("Match successful!")
            else:
                message = "Try again! 🎯"
                print("Match failed!")
            
            # Generate new challenge word after every attempt
            new_challenge = random.choice(["python", "emoji", "rocket", "train", "erwin"])
            # Make sure we don't get the same word twice
            while new_challenge.lower() == challenge_word.lower():
                new_challenge = random.choice(["python", "emoji", "rocket", "train", "erwin"])
            session["challenge_word"] = new_challenge
            challenge_word = new_challenge  # Update for this response
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
