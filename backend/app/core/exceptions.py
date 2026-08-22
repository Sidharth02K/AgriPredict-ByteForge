from fastapi import Request
from fastapi.responses import JSONResponse


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Return a consistent JSON response for unexpected server errors.
    """

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred.",
            "path": request.url.path,
        },
    )
