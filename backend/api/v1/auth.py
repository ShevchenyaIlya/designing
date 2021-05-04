from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import users_service as service
from services.request_validators import content_type_validation

from .documentation import auto

auth: Blueprint = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
@auto.doc()
def login() -> Tuple[Any, int]:
    """
    User login endpoint
    """

    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.user_login(body)), HTTPStatus.OK


@auth.route("/register", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.CREATE_USERS)
def register() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.user_register(body)), HTTPStatus.CREATED
