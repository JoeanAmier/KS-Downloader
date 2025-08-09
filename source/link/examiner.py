from itertools import chain
from re import compile
from typing import TYPE_CHECKING, Any
from urllib.parse import (
    parse_qs,
    urlparse,
    urlunparse,
)
from httpx import get
from ..tools import capture_error_request, retry_request, wait
from ..variable import TIMEOUT

if TYPE_CHECKING:
    from ..manager import Manager


class Examiner:
    SHORT_URL = compile(
        r"(https?://\S*kuaishou\.(?:com|cn)/[^\s\"<>\\^`{|}，。；！？、【】《》]+)"
    )
    LIVE_URL = compile(r"https?://live\.kuaishou\.com/\S+/\S+/(\S+)")
    PC_COMPLETE_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/short-video/\S+)")
    C_COMPLETE_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/fw/photo/\S+)")
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

    async def run(self, text: str, type_="detail", proxy: str = ""):
        urls = await self.__request_redirect(
            text,
            proxy,
        )
        match type_:
            case "detail":
                return self.__validate_links(
                    urls,
                )
            case "user":
                pass
            case "":
                return urls.split()
        raise ValueError

    def __validate_links(
        self,
        urls: str,
    ) -> list[str]:
        return [
            i.group()
            for i in chain(
                self.REDIRECT_URL.finditer(urls),
                self.PC_COMPLETE_URL.finditer(urls),
                self.C_COMPLETE_URL.finditer(urls),
            )
        ]

    async def __request_redirect(
        self,
        text: str,
        proxy: str = "",
    ) -> str:
        if not (urls := self.PC_COMPLETE_URL.findall(text)):
            urls = self._convert_live(text) or self.SHORT_URL.findall(text)
        result = []
        for i in urls:
            result.append(
                await self.__request_url(
                    i,
                    proxy,
                )
            )
        return " ".join(i for i in result if i)

    def _convert_live(self, text: str) -> list[str]:
        return [
            f"https://www.kuaishou.com/short-video/{i}"
            for i in self.LIVE_URL.findall(text)
        ]

    @retry_request
    @capture_error_request
    async def __request_url(
        self,
        url: str,
        proxy: str = "",
    ) -> str:
        if proxy:
            response = get(
                url,
                headers=self.pc_headers,
                proxy=proxy,
                follow_redirects=True,
                verify=False,
                timeout=TIMEOUT,
            )
        else:
            response = await self.client.get(
                url,
                headers=self.pc_headers,
            )
        await wait()
        response.raise_for_status()
        self.__update_cookie(
            response.cookies.items(),
        )
        return str(response.url)

    def __update_cookie(
        self,
        cookies,
    ) -> None:
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
                return self._extract_params_detail(
                    url,
                )

    def _extract_params_detail(
        self,
        url: str,
    ) -> tuple[bool | None, str, str]:
        url = urlparse(url)
        params = parse_qs(url.query)
        if "chenzhongtech" in url.hostname:
            return (
                False,
                params.get("userId", [""])[0],
                params.get("photoId", [""])[0],
            )
        elif "short-video" in url.path or "fw/photo" in url.path:
            return (
                True,
                "",
                url.path.split("/")[-1],
            )
        else:
            self.console.error(f"Unknown url: {urlunparse(url)}")
            return None, "", ""
