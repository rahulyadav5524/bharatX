from fastapi import Body, Header

from app.utils.country import CountryCode
from app.utils.response import APIResponse
from app.entities.search import PostSearchBody
from app.access_control.decorators import auth_required
from app.services.search import SearchVersion 



@auth_required
async def search_result(
    authorization: str = Header(...),
    body: PostSearchBody = Body(...),
) -> APIResponse:
    search_service = SearchVersion(version=body.version).get_service()

    query = body.query
    if body.country:
        query = f"Best Price of {body.query} in {CountryCode.get_country_name(body.country)}"

    results = search_service.search(query)

    return APIResponse(data=results)
