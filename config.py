# Created by: ertwrx
# Created at: 2025-04-18 14:46:20 UTC

import logging
import os
import sys
from datetime import datetime, UTC
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AppConfig:
    def __init__(self):
        # Required environment variables with their expected types
        self.required_vars = {
            'FLASK_SECRET_KEY': str,
            'FLASK_ENV': str,
            'GUNICORN_WORKERS': int,
            'FLASK_HOST': str,
            'FLASK_PORT': int
        }

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
            'PORT': self.PORT,
            'CURRENT_TIME_UTC': self.CURRENT_TIME_UTC,
            'CURRENT_USER': self.CURRENT_USER
        }

        # Set up logging as soon as config is initialized
        self.setup_logging()

    def validate_env(self) -> Dict[str, Any]:
        """
        Validate all required environment variables are present and of correct type.
        Returns: Dict of validated environment variables
        Raises: ValueError if validation fails
        """
        missing = []
        invalid_types = []
        validated_vars = {}

        for var_name, expected_type in self.required_vars.items():
            value = os.getenv(var_name)
            
            if value is None:
                missing.append(var_name)
                continue
                
            try:
                # Convert and validate type
                if expected_type == bool:
                    validated_vars[var_name] = value.lower() in ('true', '1', 'yes')
                elif expected_type == int:
                    validated_vars[var_name] = int(value)
                else:
                    validated_vars[var_name] = expected_type(value)
            except ValueError:
                invalid_types.append(f"{var_name} (expected {expected_type.__name__})")

        # Build error message if needed
        errors = []
        if missing:
            errors.append(f"Missing required variables: {', '.join(missing)}")
        if invalid_types:
            errors.append(f"Invalid type for variables: {', '.join(invalid_types)}")
            
        if errors:
            error_msg = "\n".join([
                "Configuration validation failed:",
                *errors,
                "Please check your .env file or environment settings."
            ])
            raise ValueError(error_msg)

        # Log successful validation
        logging.info("Environment validation successful")
        return validated_vars

    def get_environment_value(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        Safe method to get environment variables with type conversion
        Args:
            key: The environment variable name
            default: Default value if not found
            required: Whether the variable is required
        Returns:
            The environment variable value with proper type conversion
        """
        value = os.getenv(key, default)
        if required and value is None:
            raise ValueError(f"Required environment variable {key} is not set")
        
        if value is not None:
            # Convert to correct type based on default value if provided
            if default is not None:
                try:
                    value = type(default)(value)
                except ValueError:
                    logging.warning(f"Could not convert {key} to type {type(default)}")
                    
        return value

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

    def get_environment_status(self) -> Dict[str, Any]:
        """
        Get the current status of all environment variables
        Returns a dictionary with status information
        """
        return {
            'environment': self.FLASK_ENV,
            'debug_mode': self.DEBUG,
            'timestamp_utc': self.CURRENT_TIME_UTC,
            'user': self.CURRENT_USER,
            'host': self.HOST,
            'port': self.PORT,
            'logging_configured': bool(logging.getLogger().handlers)
        }

    def apply_config(self, app) -> None:
        """Apply configuration to Flask application."""
        app.config.update(self.FLASK_CONFIG)
        
        # Log configuration application
        logging.info(f"Applied configuration to Flask application")
        env_status = self.get_environment_status()
        logging.info(f"Environment Status: {env_status}")

    def validate_timestamp_format(self, timestamp_str: str) -> bool:
        """
        Validate if a timestamp string matches the required format
        Args:
            timestamp_str: The timestamp string to validate
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            return True
        except ValueError:
            return False

# Create a singleton instance
try:
    config = AppConfig()
    # Validate current timestamp format
    if not config.validate_timestamp_format(config.CURRENT_TIME_UTC):
        logging.warning(f"Invalid timestamp format: {config.CURRENT_TIME_UTC}")
except ValueError as e:
    logging.error(f"Configuration Error: {e}")
    sys.exit(1)
