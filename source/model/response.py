from pydantic import BaseModel


class ResponseModel(BaseModel):
    message: str
    params: BaseModel
    data: dict | None
