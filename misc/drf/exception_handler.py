from rest_framework.response import Response
from rest_framework.views import exception_handler

from misc.exceptions import DomainError


def domain_exception_handler(exc, context):
    if isinstance(exc, DomainError):
        return Response({'detail': str(exc)}, status=exc.status_code)

    return exception_handler(exc, context)
