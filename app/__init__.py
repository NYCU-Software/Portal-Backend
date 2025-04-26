from flask import Flask
from flask_cors import CORS
from .controllers import user_bp, client_bp
from .services import HydraService, KratosService


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name.capitalize()}Config")

    if app.config.get("ALLOW_CORS"):
        CORS(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(client_bp)
    app.hydra_service = HydraService(
        app.config.get("HYDRA_PUBLIC"), app.config.get("HYDRA_ADMIN")
    )
    app.kratos_service = KratosService(app.config.get("KRATOS_URL"))

    return app
