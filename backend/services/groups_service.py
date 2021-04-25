from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.groups import groups as db
from psycopg2 import Error


def select_groups() -> List:
    groups = db.select_groups()

    return groups


def select_single_group(group_id: int):
    group = db.select_group_by_id(group_id)

    if group is None:
        raise HTTPException(
            f"Group with '{group_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return group


def delete_group(group_id: int) -> Dict:
    response = db.delete_group(group_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such group does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_group(body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ['name', 'description']

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new group", HTTPStatus.BAD_REQUEST
        )

    try:
        group_id = db.insert_group(body)
    except Error:
        raise HTTPException(
            "Invalid data for creating new group", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if not group_id:
        raise HTTPException(
            "Group already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": group_id}


def update_group(group_id: int, body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    response = db.update_group(group_id, body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such group does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
