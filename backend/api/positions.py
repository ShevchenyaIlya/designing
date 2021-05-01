from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import positions_service as service
from services.request_validators import content_type_validation

positions: Blueprint = Blueprint("positions", __name__, url_prefix="/api/v1")


@positions.route("/positions", methods=["GET"])
@jwt_required()
@permissions(Permission.MANAGE_POSITIONS)
def select_units() -> Tuple[Any, int]:
    return jsonify(service.select_positions()), HTTPStatus.OK


@positions.route("/positions/<int:position_id>", methods=["GET"])
@jwt_required()
@permissions(Permission.MANAGE_POSITIONS)
def select_single_position(position_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_position(position_id)), HTTPStatus.OK


@positions.route("/positions", methods=["POST"])
@jwt_required()
@permissions(Permission.MANAGE_POSITIONS)
def insert_position() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_position(body)), HTTPStatus.OK


@positions.route("/positions/<int:position_id>", methods=["PUT", "PATCH"])
@jwt_required()
@permissions(Permission.MANAGE_POSITIONS)
def update_position(position_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_position(position_id, body)), HTTPStatus.OK


@positions.route("/positions/<int:position_id>", methods=["DELETE"])
@jwt_required()
@permissions(Permission.MANAGE_POSITIONS)
def delete_position(position_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_position(position_id)), HTTPStatus.OK
