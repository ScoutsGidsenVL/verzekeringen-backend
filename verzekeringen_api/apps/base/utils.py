from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler

from inuits.mail import MailServiceException


def exception_handler(exc, context):
    """Handle Django ValidationError as an accepted exception"""
    if isinstance(exc, DjangoValidationError):
        try:
            detail = exc.message_dict
        except Exception:
            detail = exc.messages
        exc = DRFValidationError(detail=detail)
    elif isinstance(exc, MailServiceException):
        exc = MailServiceException(exc)

    return drf_exception_handler(exc, context)
