from itertools import chain
from re import compile
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import (
    urlparse,
    parse_qs, urlunparse,
)

from ..tools import capture_error_request
from ..tools import retry_request

if TYPE_CHECKING:
    from ..manager import Manager


class Examiner:
    SHORT_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/\S+)")
    PC_COMPLETE_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/short-video/\S+)")
    REDIRECT_URL = compile(r"(https?://\S*chenzhongtech\.(?:com|cn)/fw/photo/\S+)")

    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.cookie = manager.cookie
        # self.app_headers = manager.app_headers
        # self.app_data_headers = manager.app_data_headers
        self.pc_headers = manager.pc_headers
        self.pc_data_headers = manager.pc_data_headers
        self.console = manager.console
        self.retry = manager.max_retry

    async def run(self, text: str, type_="detail"):
        urls = await self.__request_redirect(text, )
        match type_:
            case "detail":
                return self.__validate_links(urls, )
            case "user":
                pass
        raise ValueError

    def __validate_links(self, urls: str, ) -> list[str]:
        return [
            i.group()
            for i in chain(
                self.REDIRECT_URL.finditer(urls),
                self.PC_COMPLETE_URL.finditer(urls),
            )
        ]

    async def __request_redirect(self, text: str, ) -> str:
        if not (urls := self.PC_COMPLETE_URL.findall(text)):
            urls = self.SHORT_URL.findall(text)
        result = []
        for i in urls:
            result.append(await self.__request_url(i, ))
        return " ".join(i for i in result if i)

    @retry_request
    @capture_error_request
    async def __request_url(self, url: str, ) -> str:
        response = await self.client.head(
            url,
            headers=self.pc_headers,
        )
        response.raise_for_status()
        self.__update_cookie(response.cookies.items(), )
        return str(response.url)

    def __update_cookie(self, cookies, ) -> None:
        if self.cookie:
            return
        if cookies := self.__format_cookie(cookies):
            self.cookie = cookies
            # self.app_headers["Cookie"] = cookies
            # self.app_data_headers["Cookie"] = cookies
            self.pc_headers["Cookie"] = cookies
            self.pc_data_headers["Cookie"] = cookies

    @staticmethod
    def __format_cookie(cookies):
        return "; ".join([f"{key}={value}" for key, value in cookies])

    def extract_params(
            self,
            url: str,
            type_: str = "detail",
    ) -> Any:
        match type_:
            case "detail":
                return self._extract_params_detail(url, )

    def _extract_params_detail(
            self,
            url: str,
    ) -> [bool | None, str, str]:
        url = urlparse(url)
        params = parse_qs(url.query)
        if "chenzhongtech" in url.hostname:
            return (
                False,
                params.get("userId", [""])[0],
                params.get("photoId", [""])[0],
            )
        elif "short-video" in url.path:
            return (
                True,
                "",
                url.path.split("/")[-1],
            )
        else:
            self.console.error(f"Unknown url: {urlunparse(url)}")
            return None, "", ""
