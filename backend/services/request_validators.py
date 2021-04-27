from http import HTTPStatus
from typing import Dict, List

from http_exception import HTTPException
from validators import validate_content_type


def content_type_validation(content_type: str) -> None:
    if not validate_content_type(content_type):
        raise HTTPException("Unsupported media type", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)


def check_empty_request_body(body: Dict) -> None:
    """
    Check if request body is not None
    """

    if not body:
        raise HTTPException("Empty body content", HTTPStatus.BAD_REQUEST)


def check_body_content(body: Dict, *, fields: List) -> None:
    """
    Check if body contain all given in fields variable keys
    """

    if any(field not in body for field in fields):
        raise HTTPException(
            "Incorrect body content for creating new department", HTTPStatus.BAD_REQUEST
        )
