from http import HTTPStatus
from typing import Any, Tuple

from enums import Permission
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields
from permissions import permissions
from services import positions_service as service
from services.request_validators import content_type_validation

api = Namespace(
    "Positions", description="Position related endpoints", path="/api/v2/positions"
)

position_body = api.model(
    "Position",
    {
        "title": fields.String(description="Position title", required=True),
        "level": fields.Integer(description="Position level", required=True),
    },
)


@api.route("/", endpoint="positions")
class Policy(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get list of positions",
        },
        description="List positions",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POSITIONS)
    def get(self) -> Tuple[Any, int]:
        return service.select_positions(), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=position_body,
        responses={
            201: "Successfully execute creation",
            400: "Validation error. Invalid request body content",
            403: "Forbidden. Position exist or something went wrong",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new position",
        },
        description="Create new position",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POSITIONS)
    def post(self) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.insert_position(body), HTTPStatus.CREATED


@api.route("/<int:position_id>")
@api.param("position_id", "The position identifier")
class SinglePosition(Resource):
    @api.doc(
        security="apikey",
        responses={
            200: "Successfully get single position",
        },
        description="Get single position",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POSITIONS)
    def get(self, position_id: int) -> Tuple[Any, int]:
        return service.select_single_position(position_id), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=position_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such unit does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new unit",
        },
        description="Update single position",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POSITIONS)
    def put(self, position_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_position(position_id, body), HTTPStatus.OK

    @api.doc(
        security="apikey",
        body=position_body,
        responses={
            200: "Successfully execute update",
            400: "Validation error. Invalid request body content",
            409: "Conflict. Update operation have no effect. Such position does not exist",
            415: "Unsupported media type",
            422: "Unprocessable entity. Invalid data for creating new position",
        },
        description="Update single position",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_UNITS)
    def patch(self, position_id: str) -> Tuple[Any, int]:
        content_type_validation(request.headers["Content-Type"])
        body = request.get_json()

        return service.update_position(position_id, body), HTTPStatus.OK

    @api.doc(
        security="apikey",
        responses={
            200: "Successfully execute delete operation",
            409: "Delete operation have no effect. Such position does not exist",
        },
        description="Delete single position",
    )
    @jwt_required()
    @permissions(Permission.MANAGE_POSITIONS)
    def delete(self, position_id: int) -> Tuple[Any, int]:
        return service.delete_position(position_id), HTTPStatus.OK
