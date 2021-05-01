from http import HTTPStatus
from typing import Dict, List

from enums import TransactionResult
from http_exception import HTTPException
from models.position import positions as db
from services.request_validators import check_body_content, check_empty_request_body


def select_positions() -> List:
    positions = db.select_positions()

    return positions


def select_single_position(position_id: int):
    position = db.select_position_by_id(position_id)

    if position is None:
        raise HTTPException(
            f"Position with '{position_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return position


def delete_position(position_id: int) -> Dict:
    response = db.delete_position(position_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such position does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_position(body: Dict):
    check_empty_request_body(body)
    check_body_content(body, fields=["title", "level"])

    if (position_id := db.insert_position(body)) == TransactionResult.ERROR:
        raise HTTPException(
            "Invalid data for creating new position", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if position_id == TransactionResult.SUCCESS:
        raise HTTPException(
            "Position already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": position_id}


def update_position(position_id: int, body: Dict):
    check_empty_request_body(body)

    if (response := db.update_position(position_id, body)) is None:
        raise HTTPException(
            "Position with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such position does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
