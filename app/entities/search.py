from pydantic import BaseModel


class PostSearchBody(BaseModel):
    query: str
    country: str
