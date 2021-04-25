from http import HTTPStatus

from http_exception import HTTPException
from validators import validate_content_type


def content_type_validation(content_type: str):
    if not validate_content_type(content_type):
        raise HTTPException("Unsupported media type", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
