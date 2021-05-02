from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields, reqparse
from permissions import permissions
from services import users_service as service
from services.request_validators import content_type_validation

api = Namespace("Users", description="User related endpoints", path="/users")

email_body = api.model(
    "Email",
    {
        "email": fields.String(description="User email", required=True),
    },
)

user_body = api.model(
    "User",
    {
        "first_name": fields.String(description="First name", required=True),
        "last_name": fields.String(description="Last name", required=True),
        "middle_name": fields.String(description="Middle name", required=True),
        "email": fields.String(description="User email", required=True),
        "department_id": fields.Integer(
            description="Department identifier", required=True
        ),
        "unit_id": fields.String(description="Unit identifier", required=True),
        "position_id": fields.String(description="Position identifier", required=True),
    },
)

user_role_body = api.model(
    "User role",
    {
        "user_id": fields.Integer(description="User identifier", required=True),
        "role_id": fields.Integer(description="Role identifier", required=True),
    },
)

user_group_body = api.model(
    "User group",
    {
        "user_id": fields.Integer(description="User identifier", required=True),
        "group_id": fields.Integer(description="Group identifier", required=True),
    },
)


@api.route("/profile", endpoint="users")
class Users(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get current user profile",
        },
        description="User profile",
    )
    @jwt_required()
    def get(self) -> Tuple[Any, int]:
        user_identity = get_jwt_identity()

        return service.user_profile(user_identity)


@api.route("/")
class UsersOperations(Resource):
    @api.doc(
        security="apikey",
        body=email_body,
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such user does not exist",
        },
        description="Delete user",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def delete(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.delete_user(body)

    @api.doc(
        security="apikey",
        body=user_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such department does not exist",
            422: "Unprocessable entity. Invalid data for creating new department",
        },
        description="Update user profile",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def put(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_user(body)

    @api.doc(
        security="apikey",
        body=user_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such department does not exist",
            422: "Unprocessable entity. Invalid data for creating new department",
        },
        description="Update user profile",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def patch(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_user(body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of users",
        },
        description="List users",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def get(self) -> Tuple[Any, int]:
        return service.select_users()


user_role_parser = reqparse.RequestParser()
user_role_parser.add_argument("user_id", type=int)
user_role_parser.add_argument("role_id", type=int)


@api.route("/user-roles/<int:user_id>")
@api.param("user_id", "The user identifier")
class SingleUserRoles(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully select user roles ",
        },
        description="Get user roles",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def get(self, user_id: int) -> Tuple[Any, int]:
        return service.select_user_roles(user_id)


@api.route("/user-roles")
class UsersRoles(Resource):
    @api.doc(
        security="apikey",
        body=user_role_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            422: "Unprocessable entity. Invalid data for creating new user role",
        },
        description="Create new user role",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_user_role(body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such user role does not exist",
            422: "Unprocessable entity. Invalid query parameters for deleting user role",
        },
        description="Delete user role",
    )
    @api.expect(user_role_parser)
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def delete(self) -> Tuple[Any, int]:
        user_id = request.args.get("user_id", None)
        role_id = request.args.get("role_id", None)

        return service.delete_user_role(user_id, role_id)


user_group_parser = reqparse.RequestParser()
user_group_parser.add_argument("user_id", type=int)
user_group_parser.add_argument("group_id", type=int)


@api.route("/user-groups/<int:user_id>")
@api.param("user_id", "The user identifier")
class SingleUserGroups(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully select user groups",
        },
        description="Get user groups",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def get(self, user_id: int) -> Tuple[Any, int]:
        return service.select_user_groups(user_id)


@api.route("/user-groups")
class UsersGroups(Resource):
    @api.doc(
        security="apikey",
        body=user_group_body,
        responses={
            200: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            422: "Unprocessable entity. Invalid data for creating new user group",
        },
        description="Create new user group",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_user_group(body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such user group does not exist",
            422: "Unprocessable entity. Invalid query parameters for deleting user group",
        },
        description="Delete single user group",
    )
    @api.expect(user_group_parser)
    @jwt_required()
    @permissions(Permission.MANAGE_USERS)
    def delete(self) -> Tuple[Any, int]:
        user_id = request.args.get("user_id", None)
        group_id = request.args.get("group_id", None)

        return service.delete_user_group(user_id, group_id)
