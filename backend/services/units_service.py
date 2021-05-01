from http import HTTPStatus
from typing import Dict, List

from enums import TransactionResult
from http_exception import HTTPException
from models.unit import units as db
from services.request_validators import check_body_content, check_empty_request_body


def select_units(body: Dict) -> List:
    """
    If body content have department_id, than selects all department units, elsewhere select units in all departments
    """

    if (
        body is not None
        and (department_id := body.get("department_id", None)) is not None
    ):
        units = db.select_department_units(department_id)
    else:
        units = db.select_units()

    return units


def select_single_unit(unit_id: int):
    unit = db.select_single_unit(unit_id)

    if unit is None:
        raise HTTPException(
            f"Unit with '{unit_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return unit


def delete_unit(unit_id: int) -> Dict:
    response = db.delete_unit(unit_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such unit does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_unit(body: Dict):
    check_empty_request_body(body)
    check_body_content(body, fields=["name", "description", "department_id", "head_id"])

    if (unit_id := db.insert_unit(body)) == TransactionResult.ERROR:
        raise HTTPException(
            "Invalid data for creating new department", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if unit_id == TransactionResult.SUCCESS:
        raise HTTPException("Unit exist or something went wrong", HTTPStatus.FORBIDDEN)

    return {"id": unit_id}


def update_unit(unit_id: int, body: Dict):
    check_empty_request_body(body)

    if (response := db.update_unit(unit_id, body)) is None:
        raise HTTPException(
            "Unit with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such department does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
