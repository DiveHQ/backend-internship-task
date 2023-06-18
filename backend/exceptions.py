from rest_framework.exceptions import JsonResponse
from rest_framework.views import exception_handler, status

from .utils.createResponse import buildResponse, createResponse


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """

    response = exception_handler(exc, context)

    return (
        createResponse(
            message=exc.detail,
            success=False,
            status_code=exc.status_code,
        )
        if response is not None
        else createResponse(
            message="Something went wrong",
            success=False,
            status_code=500,
        )
    )


def handleNotFound(request, exception):
    """
    Generic 404 error handler.
    """
    data = buildResponse(message="Route does not exist", success=False)
    return JsonResponse(data, status=status.HTTP_404_NOT_FOUND)


def handleBadRequest(request, exception):
    """
    Generic 400 error handler.
    """
    data = buildResponse(message="Bad Request", success=False)
    return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)


def handleServerError(request):
    """
    Generic 500 error handler.
    """
    data = buildResponse(message="Internal Server Error", success=False)
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
