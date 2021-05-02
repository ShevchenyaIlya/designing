from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from permissions import permissions
from services import roles_service as service
from services.request_validators import content_type_validation

api = Namespace("Roles", description="Role related endpoints", path="/roles")

role_body = api.model(
    "Role",
    {
        "name": fields.String(description="Role name", required=True),
        "description": fields.String(description="Role description", required=True),
    },
)

role_policy_body = api.model(
    "Role policy",
    {
        "policy_id": fields.Integer(description="Policy identifier", required=True),
        "role_id": fields.Integer(description="Role identifier", required=True),
    },
)


@api.route("/", endpoint="roles")
class Roles(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of roles",
        },
        description="List roles",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self) -> Tuple[Any, int]:
        return service.select_roles()

    @api.doc(
        security="apikey",
        body=role_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Role already exist or something went wrong",
            422: "Unprocessable entity. Invalid data for creating new role",
        },
        description="Create new role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_role(body)


@api.route("/users-with-role/<int:role_id>")
@api.param("role_id", "The role identifier")
class UsersWithRole(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of users with role",
        },
        description="List users with role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, role_id: int) -> Tuple[Any, int]:
        return service.select_users_with_role(role_id)


@api.route("/<int:role_id>")
@api.param("role_id", "The role identifier")
class SingleRole(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single role",
        },
        description="Get single role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, role_id: int) -> Tuple[Any, int]:
        return service.select_single_role(role_id)

    @api.doc(
        security="apikey",
        body=role_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such role does not exist",
            422: "Unprocessable entity. Invalid data for creating new role",
        },
        description="Update single role(PUT)",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def put(self, role_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_role(role_id, body)

    @api.doc(
        security="apikey",
        body=role_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such role does not exist",
            422: "Unprocessable entity. Invalid data for creating new role",
        },
        description="Update single role(PATCH)",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def patch(self, role_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_role(role_id, body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such role does not exist",
        },
        description="Delete single role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def delete(self, role_id: int) -> Tuple[Any, int]:
        return service.delete_role(role_id)


@api.route("/policies/<int:role_id>")
@api.param("role_id", "The role identifier")
class SingleRolePolicy(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully select role policies",
        },
        description="Get role policies",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, role_id: int) -> Tuple[Any, int]:
        return service.select_role_policies(role_id)


role_policies_parser = reqparse.RequestParser()
role_policies_parser.add_argument("policy_id", type=int)
role_policies_parser.add_argument("role_id", type=int)


@api.route("/policies")
class RolePolicies(Resource):
    @api.doc(
        security="apikey",
        body=role_policy_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            422: "Unprocessable entity. Invalid data for creating new role policy",
        },
        description="Create new role policy",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_role_policy(body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such role policy does not exist",
            422: "Unprocessable entity. Invalid query parameters for deleting role policy",
        },
        description="Delete role policy",
    )
    @api.expect(role_policies_parser)
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def delete(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.delete_role_policy(body)
