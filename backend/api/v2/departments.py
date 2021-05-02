from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from permissions import permissions
from services import departments_service as service
from services.request_validators import content_type_validation

api = Namespace(
    "Departments", description="Departments related endpoints", path="/departments"
)

department_body = api.model(
    "Departments",
    {
        "name": fields.String(description="Department name"),
        "description": fields.String(description="Department description"),
        "head_id": fields.Integer(description="Head user identifier"),
    },
)


@api.route("/", endpoint="departments")
class Departments(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of departments",
        },
        description="List departments",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def get(self) -> Tuple[Any, int]:
        return service.select_departments()

    @api.doc(
        security="apikey",
        body=department_body,
        responses={
            204: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Department exist or something went wrong",
            422: "Unprocessable entity. Invalid data for creating new department",
        },
        description="Create new department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_department(body)


@api.route("/<int:department_id>")
@api.param("department_id", "The department identifier")
class SingleDepartment(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single department",
        },
        description="Get single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def get(self, department_id: int) -> Tuple[Any, int]:
        return service.select_single_department(department_id)

    @api.doc(
        security="apikey",
        body=department_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such department does not exist",
            422: "Unprocessable entity. Invalid data for creating new department",
        },
        description="Update single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def put(self, department_id: int) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_department(department_id, body)

    @api.doc(
        security="apikey",
        body=department_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such department does not exist",
            422: "Unprocessable entity. Invalid data for creating new department",
        },
        description="Update single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def patch(self, department_id: int) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_department(department_id, body)

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such department does not exist",
        },
        description="Delete single department",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_DEPARTMENTS)
    def delete(self, department_id: int) -> Tuple[Any, int]:
        return service.delete_department(department_id)
