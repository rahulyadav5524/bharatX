from fastapi import Body

from app.utils.response import APIResponse
from app.entities.search import PostSearchBody
from app.access_control.decorators import auth_required


@auth_required
async def search_result(
    body: PostSearchBody = Body(...),
) -> APIResponse:
    return APIResponse(data={"status": "awesome"})
