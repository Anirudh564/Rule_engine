from flask import Flask
from config.default import Config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirects to login page when not authenticated



def create_app(config_class=Config):
    app = Flask(__name__)

    # Import and register blueprints
    from app.routes.main_routes import main
    from app.routes.api_routes import api
    app.register_blueprint(main)
    app.register_blueprint(api, url_prefix='/api')

    return app