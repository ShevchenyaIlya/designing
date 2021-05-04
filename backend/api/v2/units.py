from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from permissions import permissions
from services import units_service as service
from services.request_validators import content_type_validation

api = Namespace("Units", description="Units related endpoints", path="/api/v2/units")

unit_body = api.model(
    "Units",
    {
        "name": fields.String(description="Department name"),
        "description": fields.String(description="Department description"),
        "department_id": fields.Integer(description="Identifier of unit department"),
        "head_id": fields.Integer(description="Head user identifier"),
    },
)


@api.route("/", endpoint="units")
class Units(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of units",
        },
        description="List units",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def get(self) -> Tuple[Any, int]:
        return service.select_units(), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=unit_body,
        responses={
            201: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Unit exist or something went wrong",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new unit",
        },
        description="Create new unit",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_unit(body), HTTPStatus.CREATED


@api.route("/<int:unit_id>")
@api.param("unit_id", "The unit identifier")
class SingleUnit(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single unit",
        },
        description="Get single unit",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def get(self, unit_id: int) -> Tuple[Any, int]:
        return service.select_single_unit(unit_id), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=unit_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such unit does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new unit",
        },
        description="Update single unit",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def put(self, unit_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_unit(unit_id, body), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=unit_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such unit does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new unit",
        },
        description="Update single unit",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def patch(self, unit_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_unit(unit_id, body), HTTPStatus.OK

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such unit does not exist",
        },
        description="Delete single unit",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def delete(self, unit_id: int) -> Tuple[Any, int]:
        return service.delete_unit(unit_id), HTTPStatus.OK


@api.route("/department-units/<int:department_id>")
@api.param("department_id", "The department identifier")
class SingleDepartmentUnits(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get department units",
        },
        description="Get department units",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def get(self, department_id: int) -> Tuple[Any, int]:
        return service.select_department_units(department_id), HTTPStatus.OK
