from http import HTTPStatus
from typing import Dict, List

from enums import TransactionResult
from http_exception import HTTPException
from models.policy import policies as db
from services.request_validators import check_body_content, check_empty_request_body


def select_policies() -> List:
    policies = db.select_policies()

    return policies


def select_single_policy(policy_id: int):
    policy = db.select_policy_by_id(policy_id)

    if policy is None:
        raise HTTPException(
            f"Policy with '{policy_id}' identifier does not exist",
            HTTPStatus.NOT_FOUND,
        )

    return policy


def delete_policy(policy_id: int) -> Dict:
    response = db.delete_policy(policy_id)

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such policy does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def insert_policy(body: Dict):
    check_empty_request_body(body)
    check_body_content(body, fields=["title", "description", "is_administrative"])

    if (policy_id := db.insert_policy(body)) == TransactionResult.ERROR:
        raise HTTPException(
            "Invalid data for creating new policy", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if policy_id == TransactionResult.SUCCESS:
        raise HTTPException(
            "Policy already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": policy_id}


def update_policy(policy_id: int, body: Dict):
    check_empty_request_body(body)

    if (response := db.update_policy(policy_id, body)) is None:
        raise HTTPException(
            "Policy with such name already exist. You can't execute update operation with this data.",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such policy does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
