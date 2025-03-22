from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from ..manager import Manager


class Detail(API):
    def __init__(
        self,
        manager: "Manager",
        user_id: str,
        detail_id: str,
    ):
        super().__init__(manager)
        self.user_id = user_id
        self.detail_id = detail_id
        self.extract_keys = (
            "data",
            "currentWork",
        )
        self.params = {
            "photoId": self.detail_id,
            "principalId": self.user_id,
        }
        self.note = "作品"
        self.api = f"{API.DOMAIN}/live_api/profile/feedbyid"

    async def run(
        self,
    ):
        await self.run_single()
        return self.items

    async def run_single(
        self,
    ):
        await super().get_data(
            self.api,
            params=self.params,
        )

    def add_item(
        self,
        items: list[dict],
        *args,
        **kwargs,
    ) -> None:
        self.items = items
