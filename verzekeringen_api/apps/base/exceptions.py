from rest_framework.exceptions import APIException


class InvalidWorkflowTransitionException(Exception):
    def __init__(self, from_status: str, to_status: str, extra: str = "Can't transition between statuses"):
        message = "Invalid workflow transition from status %s to status %s" % (
            from_status,
            to_status,
        )
        if extra:
            message += ": " + extra
        return super().__init__(message)


class InvalidWorkflowTransitionAPIException(APIException):
    status_code = 400
    default_detail = "Invalid workflow transition"
    default_code = "bad_request"

    def __init__(self, exception: InvalidWorkflowTransitionException):
        detail = str(exception)
        return super().__init__(detail)


class MailServiceException(Exception):
    def __init__(self, message):
        return super().__init__(message)
