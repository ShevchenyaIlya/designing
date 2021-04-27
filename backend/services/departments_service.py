from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.department import departments as db
from psycopg2 import Error
from services.request_validators import check_body_content, check_empty_request_body


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
    check_empty_request_body(body)
    check_body_content(body, fields=["name", "description", "head_id"])

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

    return {"id": department_id}


def update_department(department_id: int, body: Dict):
    check_empty_request_body(body)

    try:
        response = db.update_department(department_id, body)
    except Error:
        raise HTTPException(
            "Department with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such department does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
