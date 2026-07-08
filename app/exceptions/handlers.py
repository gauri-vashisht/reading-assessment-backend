from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.auth import (
    AuthenticationException,
    InvalidCredentialsException,
    InvalidTokenException,
    UnauthorizedException,
    UserAlreadyExistsException,
    UserInactiveException,
)


async def authentication_exception_handler(
    request: Request,
    exc: AuthenticationException,
):
    status_map = {
        UserAlreadyExistsException: 400,
        InvalidCredentialsException: 401,
        InvalidTokenException: 401,
        UnauthorizedException: 403,
        UserInactiveException: 403,
    }

    return JSONResponse(
        status_code=status_map.get(type(exc), 400),
        content={
            "success": False,
            "message": str(exc),
        },
    )


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
        },
    )