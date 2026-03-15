from datetime import datetime
from pydantic import BaseModel, computed_field


class ResponseModel(BaseModel):
    message: str
    params: dict
    data: dict | None

    @computed_field
    @property
    def time(self) -> str:
        """格式化后的时间字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
