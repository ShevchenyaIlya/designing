from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import users_service as service
from services.request_validators import content_type_validation

from .documentation import auto

users: Blueprint = Blueprint("users", __name__)


@users.route("/profile", methods=["GET"])
@auto.doc()
@jwt_required()
def profile() -> Tuple[Any, int]:
    user_identity = get_jwt_identity()

    return jsonify(service.user_profile(user_identity)), HTTPStatus.OK


@users.route("/users", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def delete_user() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.delete_user(body)), HTTPStatus.OK


@users.route("/users", methods=["PUT", "PATCH"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def update_user() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_user(body)), HTTPStatus.OK


@users.route("/users", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def get_users() -> Tuple[Any, int]:
    return jsonify(service.select_users()), HTTPStatus.OK


@users.route("/user-roles/<int:user_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def select_user_roles(user_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_user_roles(user_id)), HTTPStatus.OK


@users.route("/user-roles", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def set_user_role() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_user_role(body)), HTTPStatus.OK


@users.route("/user-roles", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def delete_user_role() -> Tuple[Any, int]:
    user_id = request.args.get("user_id", None)
    role_id = request.args.get("role_id", None)

    return jsonify(service.delete_user_role(user_id, role_id)), HTTPStatus.OK


@users.route("/user-groups/<int:user_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def select_user_groups(user_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_user_groups(user_id)), HTTPStatus.OK


@users.route("/user-groups", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def set_user_group() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_user_group(body)), HTTPStatus.OK


@users.route("/user-groups", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_USERS)
def delete_user_group() -> Tuple[Any, int]:
    user_id = request.args.get("user_id", None)
    group_id = request.args.get("group_id", None)

    return jsonify(service.delete_user_group(user_id, group_id)), HTTPStatus.OK
