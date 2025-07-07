from functools import wraps
from typing import Callable

from app.access_control.authentication import AuthenticationService


def auth_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        authorization = kwargs.get("authorization", None)
        if not authorization:
            return {"error": "Authorization header is required"}, 401

        valid = AuthenticationService.basic_auth(authorization)
        if not valid:
            return {"error": "Invalid credentials"}, 403

        return await func(*args, **kwargs)

    return wrapper
