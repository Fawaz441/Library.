from rest_framework.response import Response


def success_response(message=None, data=None):
    response_dict = {}
    if not message and data is None:
        return Response(status=200)
    if message:
        response_dict['message'] = message
    if data is not None:
        response_dict['data'] = data
    return Response(data=response_dict, status=200)


def error_response(error=None):
    response_dict = {}
    if error:
        response_dict['error'] = error
    return Response(data=response_dict, status=400)
