# Word Train WebApp

A fun and interactive vocabulary training app, built with Flask and Gunicorn, ready for seamless deployment using Docker.

---

## Features

- Modern Flask web application
- Supports running with Flask’s development server, Gunicorn (production), or Docker
- Environment configurable via `.env`
- Integrates with public APIs for random word generation and dictionary lookup
- Easy, secure setup and deployment

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Run with Python](#run-with-python)
  - [Run with Flask](#run-with-flask)
  - [Run with Gunicorn](#run-with-gunicorn)
  - [Run with Docker](#run-with-docker)
- [Generating a Secure Secret Key](#generating-a-secure-secret-key)
- [Third-Party APIs Used](#third-party-apis-used)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Attribution & Disclaimer](#attribution--disclaimer)

---

## Requirements

- Python 3.12
- pip
- (Optional) Docker 23.x or newer

---

## Installation

```bash
git clone https://github.com/ertwrx/word_train_webapp.git
cd word_train_webapp

# (Recommended) Create and activate a virtual environment:
python3.12 -m venv venv
source venv/bin/activate

# Install Python dependencies:
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Configuration

1. **Create your environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` as needed:**

   Set your secrets, database URLs, Flask/Gunicorn settings, etc.

   Example:
   ```ini
   FLASK_APP=wsgi:app
   FLASK_ENV=development
   FLASK_DEBUG=1
   FLASK_HOST=0.0.0.0
   FLASK_PORT=5000
   GUNICORN_WORKERS=3
   GUNICORN_THREADS=2
   GUNICORN_WORKER_CLASS=sync
   GUNICORN_TIMEOUT=30
   SECRET_KEY=your_secret_key_here
   ```

   **Never commit your `.env` to version control!**

---

## Usage

### Run with Python

For basic testing (not recommended for production):

```bash
python wsgi.py
```
Or, if your app entry is inside `app/main.py`:
```bash
python app/main.py
```

---

### Run with Flask

For development only:

```bash
export FLASK_APP=wsgi:app
export FLASK_ENV=development
flask run
```
Or use your `.env`:
```bash
export $(grep -v '^#' .env | xargs)
flask run
```

---

### Run with Gunicorn

Recommended for production environments.

```bash
# With environment variables loaded from .env
export $(grep -v '^#' .env | xargs)
gunicorn -c gunicorn.conf.py wsgi:app
```

Or with explicit arguments:

```bash
gunicorn -w 3 --threads 2 --worker-class sync --timeout 30 -b 0.0.0.0:5000 wsgi:app
```

---

### Run with Docker

1. **Build the image:**
   ```bash
   docker build -t word-train-webapp .
   ```

2. **Run the container with your `.env`:**
   ```bash
   docker run --env-file .env -p 5000:5000 word-train-webapp
   ```

3. **Access the app:**  
   Open [http://localhost:5000](http://localhost:5000) in your browser.

**Note:**  
`.env` is not copied into the image; it is injected at runtime.  
For more complex setups, consider using Docker Compose.

---

## Generating a Secure Secret Key

For security, you should set a strong `SECRET_KEY` in your `.env` file.
A helper script is provided:

```bash
python generate_secret.py
```

Copy the output and paste it into your `.env` as:

```ini
SECRET_KEY=your_generated_secret_here
```

---

## Third-Party APIs Used

This app uses the following free public APIs:

- [Random Word API](https://random-word-api.vercel.app/) – for generating random words.
- [Free Dictionary API](https://dictionaryapi.dev/) – for fetching word definitions.

**Note:**  
API usage is subject to the terms and conditions of the respective providers.  
This project is for learning and personal use only.

---

## Development

- Use `.env` for configuration.
- Source your virtual environment before development.
- Use `flask run --reload` or `gunicorn --reload` for auto-reloading.

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Create a new Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Attribution & Disclaimer

This application and all of its ideas are original creations by [ertwrx](https://github.com/ertwrx).  
Any resemblance to other projects or applications is purely coincidental.

**Legal Notice:**  
This project is created for educational and learning purposes only.  
It makes use of public APIs in a manner consistent with their terms for personal and non-commercial use.  
If you are the owner of an API or resource used here and have concerns, please contact the maintainer.

---
