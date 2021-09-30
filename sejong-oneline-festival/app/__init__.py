"""
Application Factory Module
"""
from datetime import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask.json import JSONEncoder
from bson.objectid import ObjectId
from app import api

from app.api.template import template as template_bp
from app.api.error_handler import error_handler as error_bp
from app.api.api_v1 import api_v1 as api_v1_bp
from app.api.auth import auth as auth_bp

jwt_manager = JWTManager()
cors = CORS()

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%m:%S")
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return super().default(obj)


def create_app(config):
    app = Flask(
        import_name=__name__,
        instance_relative_config=True,
        static_url_path='/',
        static_folder='asset/',
        template_folder='asset/'
    )

    app.json_encoder = CustomJSONEncoder
    app.config.from_object(config)
    config.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)
    cors.init_app(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(api_v1_bp, url_prefix='/api')

    return app