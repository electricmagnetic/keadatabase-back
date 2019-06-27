from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler

def exception_handler(exception, context):
    """Handle Django ValidationError as an accepted exception"""

    if isinstance(exception, DjangoValidationError):
        if hasattr(exception, 'message_dict'):
            exception = DRFValidationError(detail=exception.message_dict)
        else:
            exception = DRFValidationError(detail='An unknown validation error occurred.')

    return drf_exception_handler(exception, context)
