from flask import Flask

app = Flask(__name__)

from app import main  # Import routes after app is defined

