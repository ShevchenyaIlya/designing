import os

from api.auth import auth
from api.departments import departments
from api.units import units
from api.users import users
from config import CONFIG
from flask import Flask, Response, jsonify
from flask_jwt_extended import JWTManager
from http_exception import HTTPException


def create_flask_app() -> Flask:
    """
    Factory for creating flask application instance
    """

    application = Flask(__name__)
    application.config.from_object(CONFIG)

    application.register_blueprint(auth)
    application.register_blueprint(users)
    application.register_blueprint(departments)
    application.register_blueprint(units)

    return application


application = create_flask_app()
jwt = JWTManager(application)


@application.errorhandler(HTTPException)
def handle_invalid_usage(error: HTTPException) -> Response:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.after_request
def after_request(response: Response) -> Response:
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

    return response


if __name__ == "__main__":
    application.debug = True
    application.run()
