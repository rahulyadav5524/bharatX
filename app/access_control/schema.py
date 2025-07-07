from pydantic import BaseModel


class BasicAuthCredentials(BaseModel):
    username: str
    password: str
