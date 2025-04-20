# Created by: ertwrx
# Created at: 2025-04-18 14:56:06 UTC

import os
import sys
from datetime import datetime, UTC
import logging
import uuid
import signal

VERSION = "1.0.0"

project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestIDMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request_id = str(uuid.uuid4())
        environ['REQUEST_ID'] = request_id
        logger.info(f"Request started - ID: {request_id}")
        return self.app(environ, start_response)

def graceful_shutdown(signum, frame):
    logger.info("Graceful shutdown initiated...")
    sys.exit(0)

# Only register the signal handler in the main process
if (
    os.environ.get('WERKZEUG_RUN_MAIN') == 'true'  # flask run main process
    or 'gunicorn' in os.environ.get('SERVER_SOFTWARE', '')  # gunicorn, etc
    or os.environ.get('FLASK_ENV') == 'production'  # production env
    or __name__ == "__main__"  # direct run
):
    try:
        signal.signal(signal.SIGTERM, graceful_shutdown)
    except ValueError as e:
        logger.warning(f"Could not register signal handler: {e}")

logger.info(f"Python path: {sys.path}")
logger.info(f"Project root: {project_root}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Application Version: {VERSION}")

try:
    from app.main import app
    app.wsgi_app = RequestIDMiddleware(app.wsgi_app)
    logger.info("Successfully imported app.main")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Working directory: {os.getcwd()}")
    logger.error(f"Python path: {sys.path}")
    raise

if __name__ == "__main__":
    logger.info(f"Starting Word Train WebApp v{VERSION}")
    logger.info(f"Current time (UTC): {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
