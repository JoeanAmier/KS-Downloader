from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from ..manager import Manager


class CommentCount(API):
    """
    通过 POST 请求获取评论数
    API: https://www.kuaishou.com/rest/v/photo/comment/list
    """

    API_URL = "https://www.kuaishou.com/rest/v/photo/comment/list"

    def __init__(
        self,
        manager: "Manager",
        photo_id: str,
        pcursor: str = "1106623825458",
    ):
        super().__init__(manager)
        self.photo_id = photo_id
        self.pcursor = pcursor
        self.note = "评论数"
        self.comment_count: int = -1

    async def run(self) -> int:
        """运行请求并返回评论数，失败返回 -1"""
        await self.run_single()
        return self.comment_count

    async def run_single(self):
        """发送 POST 请求"""
        json_data = {
            "photoId": self.photo_id,
            "pcursor": self.pcursor,
        }
        await super().get_data(
            self.API_URL,
            json=json_data,
            method="POST",
        )

    def deal_response(self, response: dict | None, *args, **kwargs) -> None:
        """处理响应，提取 commentCountV2"""
        if not response:
            self.comment_count = -1
            return
        # 直接提取 commentCountV2
        if isinstance(response, dict) and "commentCountV2" in response:
            self.comment_count = response["commentCountV2"]
        else:
            self.comment_count = -1
