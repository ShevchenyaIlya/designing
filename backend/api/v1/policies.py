from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from permissions import permissions
from services import policies_service as service
from services.request_validators import content_type_validation

from .documentation import auto

policies: Blueprint = Blueprint("policies", __name__)


@policies.route("/policies", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_POLICIES)
def select_policies() -> Tuple[Any, int]:
    return jsonify(service.select_policies()), HTTPStatus.OK


@policies.route("/policies/<int:policy_id>", methods=["GET"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_POLICIES)
def select_single_unit(policy_id: int) -> Tuple[Any, int]:
    return jsonify(service.select_single_policy(policy_id)), HTTPStatus.OK


@policies.route("/policies", methods=["POST"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_POLICIES)
def insert_policy() -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.insert_policy(body)), HTTPStatus.CREATED


@policies.route("/policies/<int:policy_id>", methods=["PUT", "PATCH"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_POLICIES)
def update_policy(policy_id: str) -> Tuple[Any, int]:
    content_type_validation(request.headers["Content-Type"])
    body = request.get_json()

    return jsonify(service.update_policy(policy_id, body)), HTTPStatus.OK


@policies.route("/policies/<int:policy_id>", methods=["DELETE"])
@auto.doc()
@jwt_required()
@permissions(Permission.MANAGE_POLICIES)
def delete_policy(policy_id: int) -> Tuple[Any, int]:
    return jsonify(service.delete_policy(policy_id)), HTTPStatus.OK
