from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.role import roles as db
from psycopg2 import Error


def select_roles() -> List:
    roles = db.select_roles()

    return roles


def select_single_role(role_id: int):
    role = db.select_role_by_id(role_id)

    if role is None:
        raise HTTPException(
            f"Role with '{role_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return role


def delete_role(role_id: int) -> Dict:
    response = db.delete_role(role_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such role does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_role(body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ['name', 'description']

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new role", HTTPStatus.BAD_REQUEST
        )

    try:
        role_id = db.insert_role(body)
    except Error:
        raise HTTPException(
            "Invalid data for creating new role", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if not role_id:
        raise HTTPException(
            "Role already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": role_id}


def update_role(role_id: int, body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    response = db.update_role(role_id, body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such role does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
