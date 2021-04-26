from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import groups_service as service
from services.content_type_validation import content_type_validation

groups: Blueprint = Blueprint('groups', __name__, url_prefix="/api/v1")


@groups.route('/groups', methods=["GET"])
@jwt_required()
def select_groups() -> Tuple[Any, int]:
    return jsonify(service.select_groups()), HTTPStatus.OK


@groups.route('/groups/<int:group_id>', methods=["GET"])
@jwt_required()
def select_single_group(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_group(group_id)), HTTPStatus.OK


@groups.route('/groups', methods=["POST"])
@jwt_required()
def insert_group() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_group(body)), HTTPStatus.OK


@groups.route('/groups/<int:group_id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_group(group_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_group(group_id, body)), HTTPStatus.OK


@groups.route('/groups/<int:group_id>', methods=["DELETE"])
@jwt_required()
def delete_group(group_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_group(group_id)), HTTPStatus.OK
