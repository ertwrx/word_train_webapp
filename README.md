# Word Train Webapp 🚂

A fun web app that generates word trains with graphical representations. Input any word and watch each letter become a train car—with customizable engines, affirmations, and interactive features!

## Demo
<!-- Optionally add a screenshot or GIF -->
[Demo Screenshot](Screenshot 2025-04-18 001238.png)

## Features

- **Word Train Generator:** Visualize words as animated trains.
- **Affirmations:** Get a random positive word with one click.
- **Speed Control:** Adjust train animation speed.
- **Train Theme Selection:** Choose your favorite engine (🚂, 🚀, 🛸, 🚌, etc.).
- **Challenge Word:** Try to match the random challenge word.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ertwrx/word_train_webapp.git
   cd word_train_webapp
   ```

2. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add a `.env` file. Example:
   ```
   SECRET_KEY=your_secret_key
   OTHER_CONFIG=...
   ```

5. Run the app:
   ```bash
   python app/main.py
   ```
   Visit [http://localhost:5000](http://localhost:5000)

## Docker Usage

Build and run the app with Docker:
```bash
docker build -t word-train-webapp .
docker run -p 5000:5000 word-train-webapp
```

## API Endpoints

- `/` : Main page (input words, see trains)
- `/random-word` : Get a random affirmation
- `/challenge` : Get/set challenge word

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **SVG:** Animated wheels

## Troubleshooting

- **Port in use?** Change the port in `main.py` or stop the conflicting process.
- **Missing dependencies?** Double-check your Python version and run `pip install -r requirements.txt`.

## Contributing

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit and push your changes
4. Open a pull request

## License

MIT License. See [LICENSE](LICENSE).

---

[View source on GitHub](https://github.com/ertwrx/word_train_webapp)
