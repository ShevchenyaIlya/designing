from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import units_service as service
from services.request_validators import content_type_validation

units: Blueprint = Blueprint("units", __name__, url_prefix="/api/v1")


@units.route("/units", methods=["GET"])
@jwt_required()
@permissions("Manage units")
def select_units() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.select_units(body)), HTTPStatus.OK


@units.route("/units/<int:unit_id>", methods=["GET"])
@jwt_required()
@permissions("Manage units")
def select_single_unit(unit_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_unit(unit_id)), HTTPStatus.OK


@units.route("/units", methods=["POST"])
@jwt_required()
@permissions("Manage units")
def insert_unit() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_unit(body)), HTTPStatus.OK


@units.route("/units/<int:unit_id>", methods=["PUT", "PATCH"])
@jwt_required()
@permissions("Manage units")
def update_unit(unit_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_unit(unit_id, body)), HTTPStatus.OK


@units.route("/units/<int:unit_id>", methods=["DELETE"])
@jwt_required()
@permissions("Manage units")
def delete_unit(unit_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_unit(unit_id)), HTTPStatus.OK
