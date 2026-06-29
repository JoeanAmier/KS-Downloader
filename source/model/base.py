from pydantic import BaseModel


class APIModel(BaseModel):
    cookies: str | None = None
    proxy: str | None = None
    # source: bool = False
