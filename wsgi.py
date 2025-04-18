# Created by: ertwrx
# Created at: 2025-04-18 14:56:06 UTC

import os
import sys
from datetime import datetime, UTC
import logging
import uuid    # Add this import
import signal  # Add this import

# Add version tracking at the top level
VERSION = "1.0.0"

# Add the project root directory to Python path before any local imports
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Set up basic logging before app import
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add RequestIDMiddleware class before app import
class RequestIDMiddleware:
    def __init__(self, app):
        self.app = app
        
    def __call__(self, environ, start_response):
        request_id = str(uuid.uuid4())
        environ['REQUEST_ID'] = request_id
        logger.info(f"Request started - ID: {request_id}")
        return self.app(environ, start_response)

# Add graceful shutdown handler
def graceful_shutdown(signum, frame):
    logger.info("Graceful shutdown initiated...")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGTERM, graceful_shutdown)

# Log startup information
logger.info(f"Python path: {sys.path}")
logger.info(f"Project root: {project_root}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Application Version: {VERSION}")  # Add version logging

try:
    # Now we can import from our local modules
    from app.main import app
    # Wrap the app with RequestIDMiddleware after import
    app.wsgi_app = RequestIDMiddleware(app.wsgi_app)
    logger.info("Successfully imported app.main")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Working directory: {os.getcwd()}")
    logger.error(f"Python path: {sys.path}")
    raise

if __name__ == "__main__":
    logger.info(f"Starting Word Train WebApp v{VERSION}")  # Add version to startup message
    logger.info(f"Current time (UTC): {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
