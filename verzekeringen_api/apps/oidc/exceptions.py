from rest_framework.exceptions import APIException
from requests.exceptions import HTTPError


class TokenRequestException(APIException):
    status_code = 401
    default_detail = "Token request failed"
    default_code = "token_request_failed"

    def __init__(self, http_exception: HTTPError):
        detail = "Token request failed with error: %s with message: %s" % (
            http_exception,
            http_exception.response.text,
        )
        return super().__init__(detail)
