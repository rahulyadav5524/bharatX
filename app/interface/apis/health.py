from app.utils.response import APIResponse


async def get_health() -> APIResponse:
    return APIResponse(data={"status": "awesome"})
