from functools import wraps
from typing import Callable, List

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from http_exception import HTTPException
from models.user import users as db


def permissions(permission_action: str) -> Callable:
    """
    Decorator wrapper definition
    permission_action - equivalent for policy title
    """

    def required_permissions(endpoint_handler: Callable) -> Callable:
        """
        Decorator definition
        """

        @wraps(endpoint_handler)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_identity = get_jwt_identity()
            policies = db.select_user_policies(user_identity["id"])

            if not has_permissions(permission_action, policies):
                raise HTTPException(
                    "You have no permissions for execute such operation", 403
                )

            endpoint_handler(*args, **kwargs)

        return wrapper

    return required_permissions


def has_permissions(permission_title: str, permission_list: List):
    required_permissions = filter(
        lambda a: a["title"] == permission_title, permission_list
    )

    if not len(list(required_permissions)):
        return False

    return True
