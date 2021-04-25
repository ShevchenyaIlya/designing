from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from models.policies import policies as db
from psycopg2 import Error


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
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ['title', 'description', 'is_administrative']

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new policy", HTTPStatus.BAD_REQUEST
        )

    try:
        policy_id = db.insert_policy(body)
    except Error:
        raise HTTPException(
            "Invalid data for creating new policy", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    if not policy_id:
        raise HTTPException(
            "Policy already exist or something went wrong", HTTPStatus.FORBIDDEN
        )

    return {"id": policy_id}


def update_policy(policy_id: int, body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    response = db.update_policy(policy_id, body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such policy does not exist",
            HTTPStatus.CONFLICT,
        )

    return body
