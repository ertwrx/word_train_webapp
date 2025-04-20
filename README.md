# Word Train WebApp

[![12-Factor App](https://img.shields.io/badge/12--Factor-Compliant-brightgreen?logo=checkmarx&logoColor=white)](https://12factor.net/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)

A fun, interactive vocabulary training app built with Flask and Gunicorn, ready for seamless Docker deployment.

---

## Features

- Modern Flask web app (Python 3.12)
- Runs with Flask, Gunicorn, or Docker
- Environment config via `.env` (never commit secrets!)
- Integrates with public APIs for random words/definitions
- Simple, secure setup and deployment

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/ertwrx/word_train_webapp.git
cd word_train_webapp

# (Recommended) Create a virtualenv:
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies:
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example and set your secrets:
```bash
cp .env.example .env
# Edit .env to set SECRET_KEY and other settings
```

**Never commit `.env` to version control!**

---

## Usage

### Run with Python (not for production)
```bash
python wsgi.py
# or
python app/main.py
```

### Run with Flask (development)
```bash
export FLASK_APP=wsgi:app
export FLASK_ENV=development
flask run
# or
export $(grep -v '^#' .env | xargs)
flask run
```

### Run with Gunicorn (production)
```bash
export $(grep -v '^#' .env | xargs)
gunicorn -c gunicorn.conf.py wsgi:app
# or
gunicorn -w 3 --threads 2 --worker-class sync --timeout 30 -b 0.0.0.0:5000 wsgi:app
```

### Run with Docker
```bash
# Build the image
docker build -t word-train-webapp .

# Run the container
docker run --env-file .env -p 5000:5000 word-train-webapp
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Generating a Secure Secret Key

Generate a strong key:
```bash
python generate_secret.py
```
Copy the output into your `.env`:
```
SECRET_KEY=your_generated_secret_here
```

---

## Third-Party APIs Used

- [Random Word API](https://random-word-api.vercel.app/) – random words
- [Free Dictionary API](https://dictionaryapi.dev/) – definitions

*API usage subject to provider terms. For learning/personal use only.*

---

## Development

- Use `.env` for local/dev config.
- Source your virtualenv before developing.
- Use `flask run --reload` or `gunicorn --reload` for hot reloads.

---

## Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## License

MIT License. See [LICENSE](LICENSE).

---

## Attribution & Disclaimer

Original by [ertwrx](https://github.com/ertwrx).  
For educational/personal use only.  
Concerns? Contact the maintainer.
