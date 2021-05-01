from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import groups_service as service
from services.request_validators import content_type_validation

from .documentation import auto

groups: Blueprint = Blueprint("groups", __name__, url_prefix="/api/v1")


@groups.route("/groups", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def select_groups() -> Tuple[Any, int]:
    return jsonify(service.select_groups()), HTTPStatus.OK


@groups.route("/users-in-group/<int:group_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def select_users_in_group(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_users_in_group(group_id)), HTTPStatus.OK


@groups.route("/groups/<int:group_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def select_single_group(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_group(group_id)), HTTPStatus.OK


@groups.route("/groups", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def insert_group() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_group(body)), HTTPStatus.OK


@groups.route("/groups/<int:group_id>", methods=["PUT", "PATCH"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def update_group(group_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_group(group_id, body)), HTTPStatus.OK


@groups.route("/groups/<int:group_id>", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def delete_group(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_group(group_id)), HTTPStatus.OK


@groups.route("/group-roles/<int:group_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def select_group_roles(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_group_roles(group_id)), HTTPStatus.OK


@groups.route("/group-roles", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def set_group_role() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_group_role(body)), HTTPStatus.OK


@groups.route("/group-roles", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_UNITS)
def delete_user_role() -> Tuple[Any, int]:
    group_id = request.args.get("group_id", None)
    role_id = request.args.get("role_id", None)

    return jsonify(service.delete_group_role(group_id, role_id)), HTTPStatus.OK
