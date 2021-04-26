from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.position import positions as db
from psycopg2 import Error


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
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ["title", "level"]

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new position", HTTPStatus.BAD_REQUEST
        )

    try:
        position_id = db.insert_position(body)
    except Error:
        raise HTTPException(
            "Invalid data for creating new position", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if not position_id:
        raise HTTPException(
            "Position already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": position_id}


def update_position(position_id: int, body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    response = db.update_position(position_id, body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such position does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
