from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from ..manager import Manager


class User(API):
    def __init__(
        self,
        manager: "Manager",
        user_id: str,
        p_cursor: str,
        *args,
        **kwargs,
    ):
        super().__init__(manager)
        self.user_id = user_id
        self.p_cursor = p_cursor
        self.extract_keys = ("feeds",)
        self.note = "发布"
        self.api = f"{self.DOMAIN}/rest/v/profile/feed"

    def generate_data(
        self,
        *args,
        **kwargs,
    ) -> dict:
        return {
            "user_id": self.user_id,
            "pcursor": self.p_cursor,
            "page": "profile",
        }
