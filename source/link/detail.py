from typing import TYPE_CHECKING

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

    async def run(self, url: str) -> str:
        return await self.request_url(url)

    @retry_request
    @capture_error_request
    async def request_url(
            self,
            url: str,
    ) -> str:
        response = await self.client.get(
            url,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.text
