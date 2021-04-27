from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.role import roles as db
from psycopg2 import Error
from services.request_validators import check_body_content, check_empty_request_body


def select_roles() -> List:
    roles = db.select_roles()

    return roles


def select_users_with_role(role_id: int) -> List:
    users = db.select_users_with_role(role_id)

    return users


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
    check_empty_request_body(body)
    check_body_content(body, fields=["name", "description"])

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
    check_empty_request_body(body)

    try:
        response = db.update_role(role_id, body)
    except Error:
        raise HTTPException(
            "Role with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such role does not exist",
            HTTPStatus.CONFLICT,
        )

    return body


def select_role_policies(role_id: int) -> List:
    policies = db.select_role_policies(role_id)

    return policies


def insert_role_policy(body: Dict):
    check_empty_request_body(body)
    check_body_content(body, fields=["role_id", "policy_id", "department_id"])

    try:
        role_policy_id = db.insert_role_policy(body)
    except Error:
        raise HTTPException(
            "Invalid data for adding new policy to role",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    return {"id": role_policy_id}


def delete_user_policy(body: Dict) -> Dict:
    check_empty_request_body(body)
    check_body_content(body, fields=["role_id", "policy_id", "department_id"])

    try:
        response = db.delete_role_policy(body)
    except Error:
        raise HTTPException(
            "Invalid query parameters for deleting role policy",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such role policy does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}
