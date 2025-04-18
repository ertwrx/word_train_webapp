# Created by: ertwrx
# Created at: 2025-04-18 14:56:06 UTC

from app.main import app
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting Word Train WebApp")
    logger.info(f"Current time (UTC): {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")
    
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['HOST'],
        port=app.config['PORT']
    )
