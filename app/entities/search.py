from pydantic import BaseModel


class PostSearchBody(BaseModel):
    query: str
    country: str
    version: int | None = None


class SearchResult(BaseModel):
    link: str
    prices: list[str]
    currency: str | None = None
    product_name: str | None = None
