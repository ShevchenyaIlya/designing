from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import users_service as service
from services.request_validators import content_type_validation

auth: Blueprint = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.user_login(body)), HTTPStatus.OK


@auth.route("/register", methods=["POST"])
@permissions("Create users")
def register() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.user_register(body)), HTTPStatus.NO_CONTENT
