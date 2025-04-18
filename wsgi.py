# Created by: ertwrx
# Created at: 2025-04-18 14:56:06 UTC

import os
import sys
from datetime import datetime, UTC
import logging

# Add the project root directory to Python path before any local imports
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)  # Changed from append to insert(0) to give it priority

# Set up basic logging before app import
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log startup information
logger.info(f"Python path: {sys.path}")
logger.info(f"Project root: {project_root}")
logger.info(f"Current working directory: {os.getcwd()}")

try:
    # Now we can import from our local modules
    from app.main import app
    logger.info("Successfully imported app.main")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error(f"Working directory: {os.getcwd()}")
    logger.error(f"Python path: {sys.path}")
    raise

if __name__ == "__main__":
    logger.info(f"Starting Word Train WebApp")
    logger.info(f"Current time (UTC): {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")

    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
