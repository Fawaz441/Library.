from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    if isinstance(exc, NotAuthenticated):
        return Response({"message": "You do not have the required permission to perform this action"}, status=401)
    return exception_handler(exc, context)