from typing import TYPE_CHECKING

from source.tools import capture_error_request
from source.tools import retry_request

if TYPE_CHECKING:
    from source.manager import Manager


class __DetailPage:
    def __init__(self, manager: "Manager"):
        self.session = manager.session
        self.headers = manager.pc_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.proxy = manager.proxy

    async def run(self, urls: list[str]) -> list[str]:
        result = []
        for i in urls:
            result.append(await self.request_url(i))
        return result

    @retry_request
    @capture_error_request
    async def request_url(self, url: str, ) -> str:
        async with self.session.get(url, headers=self.headers, proxy=self.proxy) as response:
            return await response.text()
