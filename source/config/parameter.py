from pathlib import Path
from typing import TYPE_CHECKING

from source.custom import PROJECT_ROOT
from source.tools import base_session
from source.tools import capture_error_request
from source.tools import retry_request
from source.variable import RETRY
from source.variable import TIMEOUT

if TYPE_CHECKING:
    from source.tools import ColorConsole
    from source.tools import Cleaner


class Parameter:
    def __init__(self,
                 console: "ColorConsole",
                 # cookie: str,
                 folder_name: str,
                 work_path: str,
                 cleaner: "Cleaner",
                 timeout=TIMEOUT,
                 max_retry=RETRY,
                 proxy: str = None,
                 cover="",
                 ):
        self.root = PROJECT_ROOT
        self.cleaner = cleaner
        self.console = console
        self.timeout = self.__check_timeout(timeout)
        self.retry = self.__check_max_retry(max_retry)
        self.proxy = proxy
        self.folder_name = self.__check_folder_name(folder_name)
        self.work_path = self.__check_work_path(work_path)
        # self.cookie = self.__check_cookie(cookie)
        self.cover = self.__check_cover(cover)

    def run(self) -> dict:
        return {
            "cleaner": self.cleaner,
            "root": self.root,
            "console": self.console,
            "timeout": self.timeout,
            "max_retry": self.retry,
            "proxy": self.proxy,
            "work_path": self.work_path,
            "folder_name": self.folder_name,
            # "cookie": self.cookie,
            "cover": self.cover,
        }

    def __check_timeout(self, timeout: int) -> int:
        if not isinstance(timeout, int) or timeout <= 0:
            self.console.warning("timeout 参数错误")
            return 10
        return timeout

    def __check_max_retry(self, max_retry: int) -> int:
        if not isinstance(max_retry, int) or max_retry < 0:
            self.console.warning("max_retry 参数错误")
            return 5
        return max_retry

    async def check_proxy(self) -> None:
        if self.proxy:
            self.proxy = await self.__check_proxy(self.proxy)

    @retry_request
    @capture_error_request
    async def __check_proxy(self, proxy: str | None) -> str | None:
        async with base_session() as session:
            async with session.get("https://www.baidu.com/", proxy=proxy) as response:
                if response.status == 200:
                    self.console.info(f"代理 {proxy} 测试成功")
                    return proxy
                self.console.error(f"代理 {proxy} 测试失败")
                return None

    def __check_work_path(self, work_path: str) -> Path:
        if not work_path:
            return self.root
        if (r := Path(work_path)).is_dir():
            return r
        if r := self.__check_root_again(r):
            return r
        self.console.warning("work_path 参数不是有效的文件夹路径，程序将使用项目根路径作为储存路径")
        return self.root

    @staticmethod
    def __check_root_again(root: Path) -> bool | Path:
        if root.resolve().parent.is_dir():
            root.mkdir()
            return root
        return False

    def __check_folder_name(self, folder_name: str) -> str:
        if n := self.cleaner.filter_name(folder_name, ""):
            return n
        self.console.warning("folder_name 参数不是有效的文件夹名称，程序将使用默认值：Download")
        return "Download"

    def __check_cookie(self, cookie: str) -> str:
        if isinstance(cookie, str):
            return cookie
        self.console.warning("cookie 参数错误")
        return ""

    def __check_cover(self, cover: str) -> str:
        if (c := cover.upper()) in {"", "JPEG", "WEBP"}:
            return c
        self.console.warning("cover 参数错误")
        return ""
