from typing import TYPE_CHECKING
from curl_cffi.requests import get
from ..tools import capture_error_request, retry_request, wait
from ..variable import TIMEOUT, PC_PAGE_HEADERS

if TYPE_CHECKING:
    from ..manager import Manager


class DetailPage:
    def __init__(self, manager: "Manager"):
        self.impersonate = manager.impersonate
        self.client = manager.client
        self.console = manager.console
        self.max_retry = manager.max_retry

    async def run(self, url: str, proxy: str = "", cookies: str = "") -> str:
        return await self.request_url(url, proxy, cookies)

    @retry_request
    @capture_error_request
    async def request_url(
        self,
        url: str,
        proxy: str = "",
        cookies: str = "",
    ) -> str:
        if proxy or cookies:
            response = get(
                url,
                headers=PC_PAGE_HEADERS | {"Cookie": cookies},
                proxy=proxy,
                allow_redirects=True,
                verify=False,
                timeout=TIMEOUT,
                impersonate=self.impersonate,
            )
        else:
            response = await self.client.get(url,)
        await wait()
        response.raise_for_status()
        return response.text
