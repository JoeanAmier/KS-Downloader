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
        self.client = manager.client
        self.app_headers = manager.app_headers
        self.app_data_headers = manager.app_data_headers
        self.pc_headers = manager.pc_headers
        self.pc_data_headers = manager.pc_data_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.app_url = (
            self.V_SHORT_URL,
            self.F_SHORT_URL,
        )
        self.pc_url = (
            self.PC_COMPLETE_URL,
        )

    async def run(self, text: str, key="detail"):
        app = True
        if not (urls := await self.__request_redirect(text, app, )):
            app = not app
            urls = await self.__request_redirect(text, app, )
        if not urls:
            self.console.warning("提取作品链接失败")
            return None, []
        match key:
            case "detail":
                return self.__link_judgment(urls, app, )
            case "user":
                pass
        raise ValueError

    def __link_judgment(self, urls: str, app: bool, ) -> [bool, list]:
        if app:
            urls = [i.group() for i in chain(
                self.DETAIL_URL.finditer(urls),
                self.PC_COMPLETE_URL.finditer(urls),
            )]
        else:
            urls = [i.group() for i in self.PC_COMPLETE_URL.finditer(urls)]
        return app, urls

    async def __request_redirect(self, text: str, app=True, ) -> str:
        match app:
            case True:
                urls = chain(*(i.finditer(text) for i in self.app_url))
            case False:
                urls = chain(*(i.finditer(text) for i in self.pc_url))
            case _:
                raise TypeError
        result = []
        for i in urls:
            result.append(await self.__request_url(i.group(), ))
        return " ".join(i for i in result if i)

    @retry_request
    @capture_error_request
    async def __request_url(self, url: str, ) -> str:
        response = await self.client.get(url,
                                         headers=self.app_headers if (
                                                 "https://v.kuaishou.com/" in url) else self.pc_headers,
                                         )
        response.raise_for_status()
        self.__update_cookie(response.cookies.items(), )
        return str(response.url)

    def __update_cookie(self, cookies, ) -> None:
        if cookies := self.__format_cookie(cookies):
            self.app_headers["Cookie"] = cookies
            self.app_data_headers["Cookie"] = cookies
            self.pc_headers["Cookie"] = cookies
            self.pc_data_headers["Cookie"] = cookies

    @staticmethod
    def __format_cookie(cookies):
        return "; ".join([f"{key}={value}" for key, value in cookies])
