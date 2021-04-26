from http import HTTPStatus
from typing import Dict, List, Optional

from flask_jwt_extended import create_access_token
from http_exception import HTTPException
from models.user import users as db
from psycopg2 import Error
from validators import validate_password
from werkzeug.security import check_password_hash, generate_password_hash


def user_login(body: Dict) -> Dict:
    if not body.get("email", False) or not body.get("password", False):
        raise HTTPException(f"Incorrect body content {body}!", HTTPStatus.BAD_REQUEST)

    email = body["email"]
    password = body["password"]

    user = db.find_user_by_email(email)

    if user is None:
        raise HTTPException(
            f"User with such email: '{email}' not found!", HTTPStatus.NOT_FOUND
        )

    if not check_password_hash(user[-1], password):
        raise HTTPException("Wrong password", HTTPStatus.UNAUTHORIZED)

    identity = {
        "id": user[0],
        "email": email,
    }

    access_token = create_access_token(identity=identity)

    return {
        "token": access_token,
        "email": email,
        "id": user[0],
    }


def user_register(body: Dict) -> str:
    fields = ["first_name", "last_name", "middle_name", "email", "password"]

    if any(field not in body for field in fields):
        raise HTTPException("Incorrect body content", HTTPStatus.BAD_REQUEST)

    if validate_password(body["password"]) is None:
        raise HTTPException(
            "Password must be at least 8 characters long and contain: upper and lower case characters, "
            "numbers and symbols '@#$%^&+=.!'",
            HTTPStatus.FORBIDDEN,
        )

    body["password"] = generate_password_hash(body["password"])
    user_id = db.insert_user(body)

    if not user_id:
        raise HTTPException(
            "User exist or reached company members limit", HTTPStatus.FORBIDDEN
        )

    return user_id


def user_profile(user_identity: Dict) -> Dict:
    user = db.select_user(user_identity["email"])

    if not user:
        raise HTTPException("Such user does not exist", HTTPStatus.CONFLICT)

    return user


def delete_user(body: Dict) -> Dict:
    if not body.get("email", False):
        raise HTTPException(f"Incorrect body content {body}!", HTTPStatus.BAD_REQUEST)

    response = db.delete_user(body["email"])

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such user does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def update_user(body: Dict) -> Dict:
    if not body:
        raise HTTPException("Empty body", HTTPStatus.BAD_REQUEST)

    if not body.get("email", False):
        raise HTTPException("Body must contain user email", HTTPStatus.BAD_REQUEST)

    response = db.update_user(body)

    if not response:
        raise HTTPException(
            "Update operation have no effect. Such user does not exist",
            HTTPStatus.CONFLICT,
        )

    return body


def select_users() -> Dict:
    response = db.select_users()

    return response


def select_user_roles(user_id: int) -> List:
    roles = db.select_user_roles(user_id)

    return roles


def insert_user_role(body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ["user_id", "role_id"]

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for adding new user role", HTTPStatus.BAD_REQUEST
        )

    try:
        user_role_id = db.insert_user_role(body["user_id"], body["role_id"])
    except Error:
        raise HTTPException(
            "Invalid data for adding new user role", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    return {"id": user_role_id}


def delete_user_role(user_id: Optional[int], role_id: Optional[int]) -> Dict:
    if user_id is None or role_id is None:
        raise HTTPException(
            "No query parameters for deleting user role",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    try:
        response = db.delete_user_role(user_id, role_id)
    except Error:
        raise HTTPException(
            "Invalid query parameters for deleting user role",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such user role does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}


def select_user_groups(user_id: int) -> List:
    roles = db.select_user_groups(user_id)

    return roles


def insert_user_group(body: Dict):
    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)

    fields = ["user_id", "group_id"]

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for adding user to group", HTTPStatus.BAD_REQUEST
        )

    try:
        user_group_id = db.insert_user_group(body["user_id"], body["group_id"])
    except Error:
        raise HTTPException(
            "Invalid data for adding user to group", HTTPStatus.UNPROCESSABLE_ENTITY
        )

    return {"id": user_group_id}


def delete_user_group(user_id: Optional[int], group_id: Optional[int]) -> Dict:
    if user_id is None or group_id is None:
        raise HTTPException(
            "No query parameters for deleting user group",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    try:
        response = db.delete_user_group(user_id, group_id)
    except Error:
        raise HTTPException(
            "Invalid query parameters for deleting user group",
            HTTPStatus.UNPROCESSABLE_ENTITY,
        )

    if not response:
        raise HTTPException(
            "Delete operation have no effect. Such user group does not exist",
            HTTPStatus.CONFLICT,
        )

    return {}
