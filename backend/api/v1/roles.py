from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import roles_service as service
from services.request_validators import content_type_validation

from .documentation import auto

roles: Blueprint = Blueprint("roles", __name__)


@roles.route("/roles", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def select_roles() -> Tuple[Any, int]:
    return jsonify(service.select_roles()), HTTPStatus.OK


@roles.route("/users-with-role/<int:role_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def select_users_with_roles(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_users_with_role(role_id)), HTTPStatus.OK


@roles.route("/roles/<int:role_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def select_single_role(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_role(role_id)), HTTPStatus.OK


@roles.route("/roles", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def insert_role() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_role(body)), HTTPStatus.CREATED


@roles.route("/roles/<int:role_id>", methods=["PUT", "PATCH"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def update_role(role_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_role(role_id, body)), HTTPStatus.OK


@roles.route("/roles/<int:role_id>", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def delete_role(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_role(role_id)), HTTPStatus.OK


@roles.route("/roles/policies/<int:role_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def select_role_policies(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_role_policies(role_id)), HTTPStatus.OK


@roles.route("/roles/policies", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def set_role_policy() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_role_policy(body)), HTTPStatus.OK


@roles.route("/roles/policies", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_ROLES)
def delete_role_policy() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.delete_role_policy(body)), HTTPStatus.OK
