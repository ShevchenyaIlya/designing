from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import departments_service as service
from services.request_validators import content_type_validation

departments: Blueprint = Blueprint("departments", __name__, url_prefix="/api/v1")


@departments.route("/departments", methods=["GET"])
@jwt_required()
def select_departments() -> Tuple[Any, int]:
    return jsonify(service.select_departments()), HTTPStatus.OK


@departments.route("/departments/<int:department_id>", methods=["GET"])
@jwt_required()
def select_single_department(department_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_department(department_id)), HTTPStatus.OK


@departments.route("/departments", methods=["POST"])
@jwt_required()
def insert_department() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_department(body)), HTTPStatus.OK


@departments.route("/departments/<int:department_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_department(department_id: int) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_department(department_id, body)), HTTPStatus.OK


@departments.route("/departments/<int:department_id>", methods=["DELETE"])
@jwt_required()
def delete_department(department_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_department(department_id)), HTTPStatus.OK
