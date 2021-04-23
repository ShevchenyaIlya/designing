from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models import departments as db
from psycopg2 import Error


def select_departments() -> List:
    departments = db.select_departments()

    return departments


def select_single_department(department_id: int):
    department = db.select_department_by_id(department_id)

    if department is None:
        raise HTTPException(
            f"Department with '{department_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return department


def delete_department(department_id: int) -> Dict:
    response = db.delete_department(department_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such department does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_department(body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ['name', 'description', 'head_id']

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new department", HTTPStatus.BAD_REQUEST
        )

    try:
        department_id = db.insert_department(body)
    except Error:
        raise HTTPException(
            "Invalid data for creating new department", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if not department_id:
        raise HTTPException(
            "Department exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return department_id


def update_department(department_id: int, body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    response = db.update_department(department_id, body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such department does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
