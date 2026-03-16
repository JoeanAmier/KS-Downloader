import json
import re
from typing import TYPE_CHECKING

from ..tools import capture_error_request, retry_request, wait
from ..translation import _

if TYPE_CHECKING:
    from ..manager import Manager


class CollectionCount:
    """
    通过 GET 请求获取收藏数
    从 HTML 中的 window.INIT_STATE 提取 collectionCount
    URL: https://v.m.chenzhongtech.com/fw/photo/{photoId}
    """

    API_URL_TEMPLATE = "https://v.m.chenzhongtech.com/fw/photo/{}"
    INIT_STATE_PATTERN = re.compile(r"window\.INIT_STATE\s*=\s*({.*?});", re.DOTALL)

    def __init__(
        self,
        manager: "Manager",
        photo_id: str,
    ):
        self.client = manager.client
        self.headers = manager.pc_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.photo_id = photo_id
        self.note = "收藏数"
        self.collection_count: int = -1

    async def run(self) -> int:
        """运行请求并返回收藏数，失败返回 -1"""
        await self.run_single()
        return self.collection_count

    @retry_request
    @capture_error_request
    async def run_single(self):
        """发送 GET 请求并提取 collectionCount"""
        url = self.API_URL_TEMPLATE.format(self.photo_id)
        response = await self.client.get(
            url,
            headers=self.headers,
        )
        await wait()
        response.raise_for_status()
        html = response.text
        self._extract_collection_count(html)

    def _extract_collection_count(self, html: str) -> None:
        """从 HTML 中提取 window.INIT_STATE 并解析 collectionCount"""
        if not html:
            self.collection_count = -1
            return

        # 查找 window.INIT_STATE
        match = self.INIT_STATE_PATTERN.search(html)
        if not match:
            self.console.warning(_("未找到 window.INIT_STATE"))
            self.collection_count = -1
            return

        try:
            init_state = json.loads(match.group(1))
            # 从 INIT_STATE 中提取 collectionCount
            collection_count = self._find_collection_count(init_state)
            if collection_count is not None:
                self.collection_count = collection_count
            else:
                self.collection_count = -1
        except json.JSONDecodeError as e:
            self.console.error(_("解析 INIT_STATE JSON 失败: {error}").format(error=e))
            self.collection_count = -1

    def _find_collection_count(self, data: dict) -> int | None:
        """在 INIT_STATE 数据中查找 collectionCount"""
        # 尝试常见路径
        # 路径1: 直接在根级别
        if "collectionCount" in data:
            return data["collectionCount"]

        # 路径2: 在 photo 对象中
        if "photo" in data and isinstance(data["photo"], dict):
            photo = data["photo"]
            if "collectionCount" in photo:
                return photo["collectionCount"]

        # 路径3: 在 visionVideoDetail 中
        if "visionVideoDetail" in data and isinstance(data["visionVideoDetail"], dict):
            detail = data["visionVideoDetail"]
            if "collectionCount" in detail:
                return detail["collectionCount"]

        # 路径4: 递归查找（备选）
        return self._recursive_find(data, "collectionCount")

    def _recursive_find(self, obj: dict | list, key: str) -> int | None:
        """递归查找指定 key"""
        if isinstance(obj, dict):
            if key in obj:
                return obj[key]
            for v in obj.values():
                result = self._recursive_find(v, key)
                if result is not None:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = self._recursive_find(item, key)
                if result is not None:
                    return result
        return None
