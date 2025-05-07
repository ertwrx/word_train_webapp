# 🚂 Word Train WebApp 

[![12-Factor App](https://img.shields.io/badge/12--Factor-Compliant-brightgreen?logo=checkmarx&logoColor=white)](https://12factor.net/)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-yellow?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web_App-red?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI_Server-green?logo=gunicorn&logoColor=white)](https://gunicorn.org/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-Ready-informational?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Environment Config](https://img.shields.io/badge/Environment-Config-success?logo=dotenv&logoColor=white)](https://pypi.org/project/python-dotenv/)
[![MIT License](https://img.shields.io/badge/License-MIT-lightgrey?logo=opensourceinitiative&logoColor=white)](LICENSE)

A fun, interactive vocabulary training app built with Flask and Gunicorn, ready for seamless Docker deployment.

---

## ✨ Features

- 🚀 Modern Flask web app (Python 3.12)
- 🔄 Runs with Flask, Gunicorn, or Docker
- 🔐 Environment config via `.env` (never commit secrets!)
- 📚 Integrates with public APIs for random words/definitions
- ⚡ Simple, secure setup and deployment

---

## ⚡ Quick Start

### 1️⃣ Clone & Install

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

### 2️⃣ Configure Environment

Copy the example and set your secrets:
```bash
cp .env.example .env
# Edit .env to set SECRET_KEY and other settings
```

**❗ Never commit `.env` to version control!**

---

### 🗝️ Generating a Secure Secret Key

Generate a strong key:
```bash
python generate_secret.py
```
Copy the output into your `.env`:
```
SECRET_KEY=your_generated_secret_here
```

---

## ▶️ Usage

### 🐍 Run with Python (not for production)
```bash
python wsgi.py
# or
python app/main.py
```

### 🧪 Run with Flask (development)
```bash
export FLASK_APP=wsgi:app
export FLASK_ENV=development
flask run
# or
export $(grep -v '^#' .env | xargs)
flask run
```

### 🦄 Run with Gunicorn (production)
```bash
export $(grep -v '^#' .env | xargs)
gunicorn -c gunicorn.conf.py wsgi:app
# or
gunicorn -w 3 --threads 2 --worker-class sync --timeout 30 -b 0.0.0.0:5000 wsgi:app
```

### 🐳 Run with Docker
```bash
# Build the image
docker build -t word-train-webapp .

# Run the container
docker run --env-file .env -p 5000:5000 word-train-webapp
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

### 🐙 Run with Docker Compose

You can also run the application using Docker Compose:

1. 📝 Copy the example environment file and edit as needed:
   ```bash
   cp .env.example .env
   # Edit .env to set SECRET_KEY and other settings
   ```

2. 🏗️ Build and start the application:
   ```bash
   docker-compose up --build
   ```

   The app will be available at [http://localhost:5000](http://localhost:5000).

3. 🛑 To stop the application:
   ```bash
   docker-compose down
   ```

   - To run in the background (detached):
     ```bash
     docker-compose up -d
     ```
   - To view logs:
     ```bash
     docker-compose logs -f
     ```

---

## 🔧 Admin Processes

The Word Train webapp provides several administrative commands that can be run in the same environment as the application. These commands follow the 12-factor app methodology for admin processes.

### Available Commands

#### 🧹 Clear All Sessions

```bash
flask clear-sessions
```

This command clears all session data from the application, which can be useful for troubleshooting or resetting user state.

#### 📋 List Challenge Words

```bash
flask list-words
```

This command lists all challenge words available in the application.

### Running Admin Commands

#### In Development Environment

```bash
# Activate virtual environment first
source venv/bin/activate

# Set Flask application and run command
export FLASK_APP=app.main
flask clear-sessions
```

#### With Docker

```bash
# For a running container
docker exec -it word-train-container flask clear-sessions

# Or using docker-compose
docker-compose exec web flask list-words
```

#### With Docker Compose

```bash
docker-compose exec web flask clear-sessions
```

---

## 🌐 Third-Party APIs Used

- [Random Word API](https://random-word-api.vercel.app/) – random words
- [Free Dictionary API](https://dictionaryapi.dev/) – definitions

*API usage subject to provider terms. For learning/personal use only.*

---

## 🛠️ Development

- Use `.env` for local/dev config.
- Source your virtualenv before developing.
- Use `flask run --reload` or `gunicorn --reload` for hot reloads.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

MIT License. See [LICENSE](LICENSE).

---

## 🙏 Attribution & Disclaimer

Crafted by [ertwrx](https://github.com/ertwrx), with valuable assistance from AI 🤖.  
This project is intended for educational and personal use.  
