# Created by: ertwrx
# Created at: 2025-04-18 20:32:32 UTC

import os
from dotenv import load_dotenv

# Load environment variables from .env if it exists
load_dotenv()

# Server socket with fallback values
bind = f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '5000')}"

# Worker processes with fallback values
workers = int(os.getenv("GUNICORN_WORKERS", "3"))
threads = int(os.getenv("GUNICORN_THREADS", "2"))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "sync")
timeout = int(os.getenv("GUNICORN_TIMEOUT", "30"))
