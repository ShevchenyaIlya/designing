import logging
from typing import Any, Tuple

from api.v2.auth import api as api_auth
from api.v2.departments import api as api_departments
from api.v2.groups import api as api_groups
from api.v2.policies import api as api_policies
from api.v2.positions import api as api_positions
from api.v2.roles import api as api_roles
from api.v2.units import api as api_units
from api.v2.users import api as api_users
from config import CONFIG
from flask import Flask, Response, jsonify
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource
from http_exception import HTTPException

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
    }
}


def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("werkzeug").setLevel(logging.INFO)


def create_flask_app() -> Tuple[Flask, Any]:
    """
    Factory for creating flask application instance
    """

    application = Flask(__name__)
    application.config.from_object(CONFIG)
    configure_logging()

    version = application.config["APPLICATION_VERSION"]

    for module in [
        "auth",
        "departments",
        "groups",
        "policies",
        "positions",
        "roles",
        "units",
        "users",
    ]:
        api = __import__(f"api.{version}.{module}")

    api_version = getattr(api, version)

    if version == "v1":
        from api.v1.documentation import auto, doc

        application.register_blueprint(doc)
        auto.init_app(application)

        # Register blueprints
        application.register_blueprint(api_version.auth.auth)
        application.register_blueprint(
            api_version.users.users, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.departments.departments, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.units.units, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.groups.groups, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.roles.roles, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.positions.positions, url_prefix=f"/api/{version}"
        )
        application.register_blueprint(
            api_version.policies.policies, url_prefix=f"/api/{version}"
        )
    elif version == "v2":
        api = Api(
            application,
            version="1.0",
            title="RESTful API",
            description="User management system, created using python flask framework",
            contact="shevchenya.i@gmail.com",
            linense="Protected by the best license",
            default_mediatype="application/json",
            authorizations=authorizations,
            default="Specifications",
            default_label="Postman and swagger specification",
        )
        api.add_namespace(api_auth)
        api.add_namespace(api_units)
        api.add_namespace(api_departments)
        api.add_namespace(api_policies)
        api.add_namespace(api_positions)
        api.add_namespace(api_users)
        api.add_namespace(api_roles)
        api.add_namespace(api_groups)

        @api.route("/specification", endpoint="specification")
        class APISpecification(Resource):
            def get(self):
                return api.__schema__

        @api.route("/postman", endpoint="postman")
        class APIPostman(Resource):
            def get(self):
                urlvars = False  # Build query strings in URLs
                swagger = True  # Export Swagger specifications
                return api.as_postman(urlvars=urlvars, swagger=swagger)

    return application, api


application, api = create_flask_app()
jwt = JWTManager(application)


@application.errorhandler(HTTPException)
def handle_invalid_usage(error: HTTPException) -> Response:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@application.after_request
def after_request(response: Response) -> Response:
    """
    CORS signal
    """

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")

    return response


if __name__ == "__main__":
    application.debug = True
    application.run()
