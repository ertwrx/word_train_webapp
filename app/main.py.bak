from flask import Flask, request, render_template, session
import random

app = Flask(__name__)
app.secret_key = 'secret'  # Required for session

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

    train = engine  # Start with the selected engine emoji
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
        # Add wheel after each letter
        train += style + wheel_svg
    return train

@app.route("/", methods=["GET", "POST"])
def index():
    output = None
    challenge_word = random.choice(["python", "flask", "emoji", "rocket", "train"])
    message = ""
    speed = 12  # ✅ Default value always set first

    if request.method == "POST":
        user_word = request.form["word"]
        print(f"Received word: {user_word}")  # Log received word
        engine = request.form.get("engine", "🚂")
        speed = int(request.form.get("speed", 12))  # ✅ Override with user input

        words = [w.strip() for w in user_word.splitlines() if w.strip()]
        output = [generate_word_train(word, engine) for word in words]

        session.setdefault("history", [])
        session["history"].append(user_word)

        if user_word.lower() == challenge_word.lower():
            message = "Nice! You matched the challenge!"
        else:
            message = "Try again!"

    return render_template("index.html", output=output, message=message, challenge_word=challenge_word, speed=speed)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
