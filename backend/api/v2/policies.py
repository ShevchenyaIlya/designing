from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from permissions import permissions
from services import policies_service as service
from services.request_validators import content_type_validation

api = Namespace(
    "Policies", description="Policy related endpoints", path="/api/v2/policies"
)

policy_body = api.model(
    "Policy",
    {
        "title": fields.String(description="Policy title", required=True),
        "description": fields.String(description="Policy description", required=True),
        "is_administrative": fields.Boolean(
            description="Is administrative", required=True
        ),
    },
)


@api.route("/", endpoint="policies")
class Policies(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of policies",
        },
        description="List policies",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def get(self) -> Tuple[Any, int]:
        return service.select_policies()

    @api.doc(
        security="apikey",
        body=policy_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Policy already exist or something went wrong",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new policy",
        },
        description="Create new policy",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_policy(body)


@api.route("/<int:policy_id>")
@api.param("policy_id", "The policy identifier")
class SingleDepartment(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single policy",
        },
        description="Get single policy",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def get(self, policy_id: int) -> Tuple[Any, int]:
        return service.select_single_policy(policy_id)

    @api.doc(
        security="apikey",
        body=policy_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such policy does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new policy",
        },
        description="Update single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def put(self, policy_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_policy(policy_id, body)

    @api.doc(
        security="apikey",
        body=policy_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such policy does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new policy",
        },
        description="Update single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def patch(self, policy_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_policy(policy_id, body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such policy does not exist",
        },
        description="Delete single policy",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POLICIES)
    def delete(self, policy_id: int) -> Tuple[Any, int]:
        return service.delete_policy(policy_id)
