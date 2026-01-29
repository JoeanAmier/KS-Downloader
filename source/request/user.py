from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from ..manager import Manager


class User(API):
    def __init__(
        self,
        manager: "Manager",
        cookie: str = "",
        proxy: str = "",
        user_id: str = ...,
        cursor: str = "",
    ):
        super().__init__(manager, cookie, proxy)
        self.user_id = user_id
        self.cursor = cursor
        self.extract_keys = ("feeds",)
        self.note = "发布"
        self.api = f"{self.DOMAIN}/rest/v/profile/feed"

    # def set_referer(self, referer: str = None) -> None:
    #     super().set_referer(
    #         f"https://www.kuaishou.com/profile/{self.user_id}?source=NewReco"
    #     )

    def generate_data(
        self,
        *args,
        **kwargs,
    ) -> dict:
        return {
            "user_id": self.user_id,
            "pcursor": self.cursor,
            "page": "profile",
        }
