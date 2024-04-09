from itertools import chain
from re import compile
from typing import TYPE_CHECKING

from source.tools import capture_error_request
from source.tools import retry_request

if TYPE_CHECKING:
    from source.manager import Manager


class Examiner:
    V_SHORT_URL = compile(r"(https?://v\.kuaishou\.com/\S+)")
    F_SHORT_URL = compile(r"(https?://www\.kuaishou\.com/f/\S+)")
    PC_COMPLETE_URL = compile(r"(https?://www\.kuaishou\.com/short-video/\S+)")
    DETAIL_URL = compile(r"(https?://v\.m\.chenzhongtech\.com/fw/photo/\S+)")

    def __init__(self, manager: "Manager"):
        self.session = manager.session
        self.headers = manager.app_headers
        self.data_headers = manager.app_data_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.proxy = manager.proxy

    async def run(self, text: str, key="detail") -> list:
        urls = await self.__request_redirect(text)
        if not urls:
            return []
        match key:
            case "detail":
                return [i.group() for i in self.DETAIL_URL.finditer(urls)]
            case "user":
                pass
        raise ValueError

    async def __request_redirect(self, text: str) -> str:
        urls = chain(
            self.V_SHORT_URL.finditer(text),
            self.F_SHORT_URL.finditer(text),
            # self.COMPLETE_URL.finditer(text),
        )
        result = []
        for i in urls:
            result.append(await self.__request_url(i.group()))
        return " ".join(i for i in result if i)

    @retry_request
    @capture_error_request
    async def __request_url(self, url: str) -> str:
        async with self.session.get(url, headers=self.headers, proxy=self.proxy) as response:
            self.__update_cookie(response.cookies.items())
            return str(response.url)

    def __update_cookie(self, cookies) -> None:
        if cookies := self.__format_cookie(cookies):
            self.headers["Cookie"] = cookies
            self.data_headers["Cookie"] = cookies

    @staticmethod
    def __format_cookie(cookies):
        return "; ".join([f"{key}={value.value}" for key, value in cookies])
