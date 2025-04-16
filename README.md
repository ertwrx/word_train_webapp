# Word Train Webapp 🚂

A fun web app that generates word trains with graphical representations. This app allows users to input words and see them transformed into a train, with each letter represented by a "train car" (styled as spinning wheels). Users can select the train's speed, choose a theme (engine), and even get a random word generated from an affirmation API!

## Features

- **Word Train Generator**: Converts any inputted word(s) into a visual train with spinning wheels.
- **Affirmations**: Click the "Random Word" button to generate a random affirmation.
- **Speed Control**: Adjust the speed of the train with a slider.
- **Train Theme Selection**: Choose between different "engines" like 🚂, 🚀, 🛸, 🚌, and more!
- **Challenge Word**: Match a random challenge word for a fun challenge.

## Demo

View the app in action at [Word Train Webapp Demo](http://10.0.2.15:5000/) (replace with live link if available).

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/ertwrx/word-train-webapp.git
   cd word-train-webapp

Set up a virtual environment (optional but recommended):

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the Flask app:

bash
Copy
Edit
python app/main.py
Your app should now be running at http://localhost:5000/ or http://<your-ip>:5000/.

How it Works
The user inputs words into the text box and can adjust the speed and select a train engine.

Clicking the "Generate Train" button generates a visual representation of the word train, with each letter appearing as a "train car" with a spinning wheel SVG.

The "Random Word" button fetches an affirmation from the affirmations API and generates a random word train based on that word.

The app includes a challenge feature where users try to match the challenge word, and feedback is provided based on whether the input matches the challenge word.

Technologies Used
Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript (AJAX)

SVG: Used for graphical representation of wheels

Contributing
Fork the repository

Create a new branch (git checkout -b feature-name)

Make your changes

Commit your changes (git commit -am 'Add new feature')

Push to your branch (git push origin feature-name)

Create a new pull request

License
This project is licensed under the MIT License - see the LICENSE file for details.
