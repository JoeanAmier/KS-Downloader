from typing import TYPE_CHECKING
from httpx import get
from ..tools import capture_error_request, retry_request, wait
from ..variable import TIMEOUT

if TYPE_CHECKING:
    from ..manager import Manager


class DetailPage:
    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.headers = manager.pc_headers
        self.console = manager.console
        self.retry = manager.max_retry

    async def run(self, url: str, proxy: str = "", cookie: str = "") -> str:
        return await self.request_url(url, proxy, cookie)

    @retry_request
    @capture_error_request
    async def request_url(
        self,
        url: str,
        proxy: str = "",
        cookie: str = "",
    ) -> str:
        headers = self.headers.copy()
        if cookie:
            headers["Cookie"] = cookie
        if proxy:
            response = get(
                url,
                headers=headers,
                proxy=proxy,
                follow_redirects=True,
                verify=False,
                timeout=TIMEOUT,
            )
        else:
            response = await self.client.get(
                url,
                headers=headers,
            )
        await wait()
        response.raise_for_status()
        return response.text
