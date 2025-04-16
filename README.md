# Word Train Webapp 🚂

A fun web app that generates word trains with graphical representations. This app allows users to input words and see them transformed into a train, with each letter represented by a "train car" (styled as spinning wheels). Users can select the train's speed, choose a theme (engine), and even get a random word generated from an affirmation API!

## Features

- **Word Train Generator:** Converts any inputted word(s) into a visual train with spinning wheels
- **Affirmations:** Click the "Random Word" button to generate a random affirmation
- **Speed Control:** Adjust the speed of the train with a slider
- **Train Theme Selection:** Choose between different "engines" like 🚂, 🚀, 🛸, 🚌, and more!
- **Challenge Word:** Match a random challenge word for a fun challenge

## Installation

1. Clone this repository to your local machine:
```bash
git clone https://github.com/ertwrx/word_train_webapp.git
cd word_train_webapp
```

2. Set up a virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask app:
```bash
python app/main.py
```

Your app should now be running at http://localhost:5000/ or http://127.0.0.1:5000/.

## How it Works

The application works through several key components:

1. The user inputs words into the text box and can adjust the speed and select a train engine.
2. Clicking the "Generate Train" button generates a visual representation of the word train, with each letter appearing as a "train car" with a spinning wheel SVG.
3. The "Random Word" button fetches an affirmation from the affirmations API and generates a random word train based on that word.
4. The app includes a challenge feature where users try to match the challenge word, and feedback is provided based on whether the input matches the challenge word.

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **SVG:** Used for graphical representation of wheels

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to your branch (`git push origin feature-name`)
6. Create a new pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
