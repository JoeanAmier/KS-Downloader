from pydantic import BaseModel


class APIModel(BaseModel):
    cookie: str | None = None
    proxy: str | None = None
    # source: bool = False
