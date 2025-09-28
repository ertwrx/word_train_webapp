from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Any additional configuration or blueprints can go here
    
    return app
