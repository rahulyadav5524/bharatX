import uvicorn
from fastapi import FastAPI

from app.access_control.authentication import AuthenticationService
from app.interface.routes import api_router

app = FastAPI()

AuthenticationService.set_config()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=1000,
        reload=True,
        log_level="debug",
    )
