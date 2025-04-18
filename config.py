# Created by: ertwrx
# Created at: 2025-04-18 14:46:20 UTC

import logging
import os
import sys
from datetime import datetime, UTC
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    def __init__(self):
        # Required environment variables
        self.required_vars = [
            'FLASK_SECRET_KEY',
            'FLASK_ENV',
            'GUNICORN_WORKERS',
            'FLASK_HOST',
            'FLASK_PORT'
        ]

        # Validate and load environment variables
        self.validate_env()

        # Set up configuration properties
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'production')
        self.DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        
        # Flask application settings
        self.HOST = os.getenv('FLASK_HOST', '0.0.0.0')
        self.PORT = int(os.getenv('FLASK_PORT', '5000'))
        self.SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
        self.SERVER_NAME = None

        # Current timestamp and user info
        self.CURRENT_TIME_UTC = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
        self.CURRENT_USER = os.getenv('USER', 'ertwrx')

        # Flask application config dict
        self.FLASK_CONFIG = {
            'ENV': self.FLASK_ENV,
            'DEBUG': self.DEBUG,
            'SECRET_KEY': self.SECRET_KEY,
            'HOST': self.HOST,
            'PORT': self.PORT
        }

        # Set up logging as soon as config is initialized
        self.setup_logging()

    def validate_env(self) -> None:
        """Validate all required environment variables are present."""
        missing: List[str] = [var for var in self.required_vars if not os.getenv(var)]

        if missing:
            error_msg = (
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please check your .env file or environment settings."
            )
            raise RuntimeError(error_msg)

    def setup_logging(self) -> None:
        """Configure application logging."""
        log_level = logging.DEBUG if self.DEBUG else logging.INFO

        # Create formatter
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        # Remove any existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        # Console handler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

        # File handler for errors (if not in debug mode)
        if not self.DEBUG:
            os.makedirs('logs', exist_ok=True)
            error_handler = logging.FileHandler('logs/error.log')
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            root_logger.addHandler(error_handler)

        # Log startup information
        logging.info(f"Starting application in {self.FLASK_ENV} mode")
        logging.info(f"Debug mode: {self.DEBUG}")
        logging.info(f"Current user: {self.CURRENT_USER}")
        logging.info(f"Current time (UTC): {self.CURRENT_TIME_UTC}")

    def apply_config(self, app) -> None:
        """Apply configuration to Flask application."""
        app.config.update({
            'ENV': self.FLASK_ENV,
            'DEBUG': self.DEBUG,
            'SECRET_KEY': self.SECRET_KEY,
            'HOST': self.HOST,
            'PORT': self.PORT,
            'CURRENT_TIME_UTC': self.CURRENT_TIME_UTC,
            'CURRENT_USER': self.CURRENT_USER
        })

# Create a singleton instance
config = AppConfig()
