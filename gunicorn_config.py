from app.config import config

# Export Gunicorn config
globals().update(config.get_gunicorn_config())
