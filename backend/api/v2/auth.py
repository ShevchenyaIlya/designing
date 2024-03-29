from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from permissions import permissions
from services import users_service as service
from services.request_validators import content_type_validation

api = Namespace("Auth", description="Authentication related endpoints", path="/api/v2")


login_body = api.model(
    "Login",
    {
        "email": fields.String(description="User email", required=True),
        "password": fields.String(description="User password", required=True),
    },
)

register_body = api.model(
    "Register",
    {
        "first_name": fields.String(description="First name", required=True),
        "last_name": fields.String(description="Last name", required=True),
        "middle_name": fields.String(description="Middle name", required=True),
        "email": fields.String(description="Email", required=True),
        "password": fields.String(description="Password", required=True),
    },
)


@api.route("/login", endpoint="login")
class Login(Resource):
    @api.doc(
        body=login_body,
        responses={
            200: "Successfully login",
            400: "Validation error. Invalid request body content",
            401: "Unauthorized. Wrong password",
            404: "Not found. User with such email does not exist",
            415: "Unsupported media type",
        },
        description="User login endpoint",
    )
    def post(self) -> Tuple[Any, int]:
        """
        User login endpoint. Return jwt token
        """

        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.user_login(body), HTTPStatus.OK


@api.route("/register", methods=["POST"])
class Register(Resource):
    @api.doc(
        body=register_body,
        security="apikey",
        responses={
            201: "Successfully register",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Wrong password format or user already exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating register new user",
        },
        description="User registration",
    )
    @jwt_required()
    @permissions(Permission.CREATE_USERS)
    def post(self) -> Tuple[Any, int]:
        """
        User registration
        """
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.user_register(body), HTTPStatus.CREATED
