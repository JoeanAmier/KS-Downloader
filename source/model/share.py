from datetime import datetime

from pydantic import BaseModel, computed_field


class ShortUrl(BaseModel):
    text: str
    proxy: str = ""


class UrlResponse(BaseModel):
    message: str
    urls: list[str] | None
    params: ShortUrl

    @computed_field
    @property
    def time(self) -> str:
        """格式化后的时间字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
