from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from permissions import permissions
from services import groups_service as service
from services.request_validators import content_type_validation

api = Namespace("Groups", description="Group related endpoints", path="/groups")

group_body = api.model(
    "Group",
    {
        "name": fields.String(description="Group name", required=True),
        "description": fields.String(description="Group description", required=True),
    },
)

group_role_body = api.model(
    "Group role",
    {
        "group_id": fields.Integer(description="Group identifier", required=True),
        "role_id": fields.Integer(description="Role identifier", required=True),
    },
)


@api.route("/", endpoint="groups")
class Groups(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of groups",
        },
        description="List groups",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self) -> Tuple[Any, int]:
        return service.select_groups()

    @api.doc(
        security="apikey",
        body=group_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Group already exist or something went wrong",
            422: "Unprocessable entity. Invalid data for creating new group",
        },
        description="Create new group",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_group(body)


@api.route("/users-in-group/<int:group_id>")
@api.param("group_id", "The group identifier")
class UsersInGroup(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of users in group",
        },
        description="List users in group",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, group_id: int) -> Tuple[Any, int]:
        return service.select_users_in_group(group_id)


@api.route("/<int:group_id>")
@api.param("group_id", "The group identifier")
class SingleGroup(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single group",
        },
        description="Get single group",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, group_id: int) -> Tuple[Any, int]:
        return service.select_single_group(group_id)

    @api.doc(
        security="apikey",
        body=group_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such group does not exist",
            422: "Unprocessable entity. Invalid data for creating new group",
        },
        description="Update single group(PUT)",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def put(self, group_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_group(group_id, body)

    @api.doc(
        security="apikey",
        body=group_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such group does not exist",
            422: "Unprocessable entity. Invalid data for creating new group",
        },
        description="Update single group(PATCH)",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def patch(self, group_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_group(group_id, body)

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
    def delete(self, group_id: int) -> Tuple[Any, int]:
        return service.delete_group(group_id)


@api.route("/roles/<int:group_id>")
@api.param("group_id", "The group identifier")
class SingleGroupRole(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully select group roles",
        },
        description="Get group roles",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def get(self, group_id: int) -> Tuple[Any, int]:
        return service.select_group_roles(group_id)


group_role_parser = reqparse.RequestParser()
group_role_parser.add_argument("group_id", type=int)
group_role_parser.add_argument("role_id", type=int)


@api.route("/roles")
class RolePolicies(Resource):
    @api.doc(
        security="apikey",
        body=group_role_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            422: "Unprocessable entity. Invalid data for creating new group role",
        },
        description="Create new group role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_group_role(body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such group role does not exist",
            422: "Unprocessable entity. Invalid query parameters for deleting group role",
        },
        description="Delete group role",
    )
    @api.expect(group_role_parser)
    @jwt_required()
    @permissions(Permission.MANAGE_ROLES)
    def delete(self) -> Tuple[Any, int]:
        group_id = request.args.get("group_id", None)
        role_id = request.args.get("role_id", None)

        return service.delete_group_role(group_id, role_id)
