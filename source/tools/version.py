from typing import TYPE_CHECKING

from ..static import RELEASES
from ..tools import capture_error_request, retry_request

if TYPE_CHECKING:
    from ..manager import Manager

__all__ = ["Version"]


class Version:
    STATUS_CODE = {
        1: "当前版本为最新正式版",
        2: "当前版本为最新开发版",
        3: "当前版本为最新开发版，可更新至正式版",
        4: "可更新至正式版",
    }

    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.console = manager.console
        self.retry = manager.max_retry

    @staticmethod
    def compare_versions(
        current_version: str, target_version: str, is_development: bool
    ) -> int:
        current_major, current_minor = map(int, current_version.split("."))
        target_major, target_minor = map(int, target_version.split("."))

        if target_major > current_major:
            return 4
        if target_major == current_major:
            if target_minor > current_minor:
                return 4
            if target_minor == current_minor:
                return 3 if is_development else 1
        return 2 if is_development else 1

    @retry_request
    @capture_error_request
    async def get_target_version(
        self,
    ):
        response = await self.client.get(
            RELEASES,
            timeout=5,
        )
        response.raise_for_status()
        version = str(response.url).split("/")
        if len(v := version[-1]) == 3:
            return v
