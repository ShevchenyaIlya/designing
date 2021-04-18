from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import users_service as service

users: Blueprint = Blueprint('users', __name__, url_prefix="/api/v1")


@users.route('/profile', methods=["GET"])
@jwt_required()
def profile() -> Tuple[Any, int]:
    user_identity = get_jwt_identity()

    return jsonify(service.user_profile(user_identity)), HTTPStatus.OK


@users.route('/users', methods=["DELETE"])
@jwt_required()
def delete_user() -> Tuple[Any, int]:
    body = request.get_json()

    return jsonify(service.delete_user(body)), HTTPStatus.OK


@users.route('/users', methods=["PUT", "PATCH"])
@jwt_required()
def update_user() -> Tuple[Any, int]:
    body = request.get_json()

    return jsonify(service.update_user(body)), HTTPStatus.OK


@users.route('/users', methods=["GET"])
@jwt_required()
def get_users() -> Tuple[Any, int]:
    return jsonify(service.select_users()), HTTPStatus.OK
