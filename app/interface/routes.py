from fastapi import APIRouter

from app.interface.apis.health import get_health
from app.interface.apis.search import search_result
from app.utils.http import HTTPMethod

api_router = APIRouter()

api_router.add_api_route(
    path="/health/",
    endpoint=get_health,
    tags=["Health Check"],
    methods=[HTTPMethod.GET],
)

api_router.add_api_route(
    path="/search/",
    endpoint=search_result,
    tags=["Search"],
    methods=[HTTPMethod.POST],
)
