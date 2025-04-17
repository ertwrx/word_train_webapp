import os
import logging

class Config:
    # Configuration settings
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')

    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def init_app(app):
        # Setup logging
        logging.basicConfig(level=Config.LOG_LEVEL)
        app.logger.setLevel(logging.getLevelName(Config.LOG_LEVEL))
