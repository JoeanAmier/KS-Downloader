from itertools import chain
from re import compile
from typing import TYPE_CHECKING, Any
from urllib.parse import (
    parse_qs,
    urlparse,
    urlunparse,
)

from click.testing import Result
from httpx import get
from ..tools import capture_error_request, retry_request, wait
from ..variable import TIMEOUT

if TYPE_CHECKING:
    from ..manager import Manager


class Examiner:
    URL = compile(r"(https?://[^\s\"<>\\^`{|}，。；！？、【】《》]+)")

    F_SHORT_URL = compile(
        r"(https?://\S*kuaishou\.(?:com|cn)/f/[^\s/\"<>\\^`{|}，。；！？、【】《》]+)"
    )
    V_SHORT_URL = compile(
        r"(https?://v\.kuaishou\.(?:com|cn)/[^\s/\"<>\\^`{|}，。；！？、【】《》]+)"
    )

    LIVE_DETAIL_URL = compile(r"https?://live\.kuaishou\.com/\S+/\S+/(\S+)")
    PC_DETAIL_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/short-video/\S+)")
    C_DETAIL_URL = compile(r"(https?://\S*kuaishou\.(?:com|cn)/fw/photo/\S+)")
    REDIRECT_DETAIL_URL = compile(
        r"(https?://\S*chenzhongtech\.(?:com|cn)/fw/photo/\S+)"
    )

    USER_URL = compile(r"(https?://(?:www|live)\.kuaishou\.com/profile/([^?/\s]+))")

    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.cookie = manager.cookie
        # self.app_headers = manager.app_headers
        # self.app_data_headers = manager.app_data_headers
        self.pc_headers = manager.pc_headers
        self.pc_data_headers = manager.pc_data_headers
        self.console = manager.console
        self.retry = manager.max_retry

    async def run(
        self, text: str, type_="detail", proxy: str = ""
    ) -> list[str] | list[tuple[str, str]]:
        urls = await self.__request_redirect(
            text,
            proxy,
        )
        match type_:
            case "detail":
                return self.__validate_detail_links(
                    urls,
                )
            case "user":
                return self.__validate_user_links(
                    urls,
                )
            case "":
                return urls.split()
        raise ValueError

    def __validate_detail_links(
        self,
        urls: str,
    ) -> list[str]:
        return [
            i.group()
            for i in chain(
                self.REDIRECT_DETAIL_URL.finditer(urls),
                self.PC_DETAIL_URL.finditer(urls),
                self.C_DETAIL_URL.finditer(urls),
                # self.LIVE_DETAIL_URL.finditer(urls),
            )
        ]

    def __validate_user_links(
        self,
        urls: str,
    ) -> list[tuple[str, str]]:
        urls = self.USER_URL.finditer(urls)
        return [(i.group(1), i.group(2)) for i in urls]

    async def __request_redirect(
        self,
        text: str,
        proxy: str = "",
    ) -> str:
        urls = self.URL.findall(text)
        result = []
        for i in urls:
            if (u := self.F_SHORT_URL.search(i)) or (u := self.V_SHORT_URL.search(i)):
                result.append(
                    await self.__request_url(
                        u.group(),
                        proxy,
                    )
                )
            else:
                result.append(i)
        return " ".join(i for i in result if i)

    def _convert_live(self, text: str) -> list[str]:
        return [
            f"https://www.kuaishou.com/short-video/{i}"
            for i in self.LIVE_DETAIL_URL.findall(text)
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
            case _:
                raise ValueError

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
