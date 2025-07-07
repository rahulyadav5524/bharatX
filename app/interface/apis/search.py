from fastapi import Body, Header

from app.utils.response import APIResponse
from app.entities.search import PostSearchBody
from app.access_control.decorators import auth_required
from app.services.search import SearchService


@auth_required
async def search_result(
    authorization: str = Header(...),
    body: PostSearchBody = Body(...),
) -> APIResponse:
    search_service = SearchService()

    query = body.query
    if body.country:
        query = f"{body.query} {body.country}"

    results = search_service.search(query, num_results=body.num_results)

    return APIResponse(data=results)
