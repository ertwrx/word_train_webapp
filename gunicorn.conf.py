# Created by: ertwrx
# Created at: 2025-04-18 19:33:04 UTC

import os
import multiprocessing
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Server socket
bind = f"{os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '5000')}"

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', '3'))
threads = int(os.getenv('GUNICORN_THREADS', '2'))
worker_class = os.getenv('GUNICORN_WORKER_CLASS', 'sync')
timeout = int(os.getenv('GUNICORN_TIMEOUT', '30'))

# Logging
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
loglevel = "info"

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Development settings
reload = True  # Auto-reload on code changes
capture_output = True
enable_stdio_inheritance = True

def on_starting(server):
    server.log.info(f"Starting Gunicorn server at {os.getenv('FLASK_HOST', '0.0.0.0')}:{os.getenv('FLASK_PORT', '5000')}")
    server.log.info(f"Current user: {os.getenv('USER', 'ertwrx')}")
    server.log.info(f"Worker configuration: {workers} workers, {threads} threads per worker")

