from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import roles_service as service
from services.content_type_validation import content_type_validation

roles: Blueprint = Blueprint('roles', __name__, url_prefix="/api/v1")


@roles.route('/roles', methods=["GET"])
@jwt_required()
def select_roles() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.select_roles(body)), HTTPStatus.OK


@roles.route('/roles/<int:role_id>', methods=["GET"])
@jwt_required()
def select_single_role(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_role(role_id)), HTTPStatus.OK


@roles.route('/roles', methods=["POST"])
@jwt_required()
def insert_role() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_role(body)), HTTPStatus.OK


@roles.route('/roles/<int:role_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_role(role_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_unit(role_id, body)), HTTPStatus.OK


@roles.route('/roles/<int:role_id>', methods=["DELETE"])
@jwt_required()
def delete_role(role_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_unit(role_id)), HTTPStatus.OK
