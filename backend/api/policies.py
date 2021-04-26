from http import HTTPStatus
from typing import Any, Tuple

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from services import policies_service as service
from services.content_type_validation import content_type_validation

policies: Blueprint = Blueprint("policies", __name__, url_prefix="/api/v1")


@policies.route("/policies", methods=["GET"])
@jwt_required()
def select_policies() -> Tuple[Any, int]:
    return jsonify(service.select_policies()), HTTPStatus.OK


@policies.route("/policies/<int:policy_id>", methods=["GET"])
@jwt_required()
def select_single_unit(policy_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_policy(policy_id)), HTTPStatus.OK


@policies.route("/policies", methods=["POST"])
@jwt_required()
def insert_policy() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_policy(body)), HTTPStatus.OK


@policies.route("/policies/<int:policy_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_policy(policy_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_policy(policy_id, body)), HTTPStatus.OK


@policies.route("/policies/<int:policy_id>", methods=["DELETE"])
@jwt_required()
def delete_policy(policy_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_policy(policy_id)), HTTPStatus.OK
