from flask import Flask
from .controllers import user_bp

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f"config.{config_name.capitalize()}Config")

    app.register_blueprint(user_bp)

    return app
