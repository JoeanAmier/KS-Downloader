from typing import TYPE_CHECKING
from urllib.parse import urlparse

from source.tools import capture_error_request
from source.tools import retry_request

if TYPE_CHECKING:
    from source.manager import Manager


class DetailPage:
    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.headers = manager.pc_headers
        self.console = manager.console
        self.retry = manager.max_retry

    async def run(self, urls: list[str]) -> list[[str, str]]:
        result = []
        for i in urls:
            id_ = urlparse(i).path.split("/")[-1]
            result.append((id_, await self.request_url(i)))
        return result

    @retry_request
    @capture_error_request
    async def request_url(self, url: str, ) -> str:
        response = await self.client.get(url, headers=self.headers, )
        response.raise_for_status()
        return response.text
