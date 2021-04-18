from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import users_service as service

auth: Blueprint = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST"])
def login() -> Tuple[Any, int]:
    body = request.get_json()

    return jsonify(service.user_login(body)), HTTPStatus.OK


@auth.route('/register', methods=["POST"])
def register() -> Tuple[Any, int]:
    body = request.get_json()

    return jsonify(service.user_register(body)), HTTPStatus.NO_CONTENT
