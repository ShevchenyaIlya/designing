from http import HTTPStatus
from typing import Dict, List, Optional

from enums import TransactionResult
from http_exception import HTTPException
from models.group import groups as db
from services.request_validators import check_body_content, check_empty_request_body


def select_groups() -> List:
    groups = db.select_groups()

    return groups


def select_users_in_group(group_id: int) -> List:
    users = db.select_users_in_group(group_id)

    return users


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
    check_empty_request_body(body)
    check_body_content(body, fields=["name", "description"])

    if (group_id := db.insert_group(body)) == TransactionResult.ERROR:
        raise HTTPException(
            "Invalid data for creating new group", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if group_id == TransactionResult.SUCCESS:
        raise HTTPException(
            "Group already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": group_id}


def update_group(group_id: int, body: Dict):
    check_empty_request_body(body)

    if (response := db.update_group(group_id, body)) is None:
        raise HTTPException(
            "Group with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such group does not exist",
            HTTPStatus.CONFLICT,
        )

    return body


def select_group_roles(group_id: int) -> List:
    roles = db.select_group_roles(group_id)

    return roles


def insert_group_role(body: Dict):
    check_empty_request_body(body)
    check_body_content(body, fields=["group_id", "role_id"])

    if (
        group_role_id := db.insert_group_role(body["group_id"], body["role_id"])
    ) is None:
        raise HTTPException(
            "Invalid data for adding new group role", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    return {"id": group_role_id}


def delete_group_role(group_id: Optional[int], role_id: Optional[int]) -> Dict:
    if group_id is None or role_id is None:
        raise HTTPException(
            "No query parameters for deleting group role",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if (response := db.delete_group_role(group_id, role_id)) is None:
        raise HTTPException(
            "Invalid query parameters for deleting group role",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such group role does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}
