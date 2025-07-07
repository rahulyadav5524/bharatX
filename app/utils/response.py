from typing import Any

from fastapi.responses import JSONResponse

from app.utils.serialization import serialize


class APIResponse(JSONResponse):
    def __init__(self, data: Any, message: str = "Success", **kwargs):
        content = {"message": message, "data": serialize(data)}
        super(APIResponse, self).__init__(content=content, **kwargs)
