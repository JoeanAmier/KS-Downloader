from pathlib import Path
from typing import TYPE_CHECKING

from httpx import HTTPError, TimeoutException, get

from ..static import PROJECT_ROOT
from ..translation import _
from ..variable import PC_USERAGENT, RETRY, TIMEOUT

if TYPE_CHECKING:
    from ..tools import Cleaner, ColorConsole


class Parameter:
    NO_PROXY = {
        "http://": None,
        "https://": None,
    }
    NAME_KEYS = {
        "作品类型",
        "作者昵称",
        "作者ID",
        "作品描述",
        "作品ID",
        "发布日期",
    }

    def __init__(
        self,
        console: "ColorConsole",
        cleaner: "Cleaner",
        mapping_data: dict,
        cookie: str,
        folder_name: str = "Download",
        name_format: str = "发布日期 作者昵称 作品描述",
        name_length: int = 128,
        work_path: str = "",
        timeout=TIMEOUT,
        max_retry=RETRY,
        proxy: str | dict = None,
        cover="",
        music=False,
        data_record: bool = False,
        chunk=1024 * 1024,
        user_agent=PC_USERAGENT,
        folder_mode: bool = False,
        author_archive: bool = False,
        max_workers=4,
    ):
        self.root = PROJECT_ROOT
        self.cleaner = cleaner
        self.console = console
        self.mapping_data = mapping_data or {}
        self.timeout = self.__check_timeout(timeout)
        self.retry = self.__check_max_retry(max_retry)
        self.proxy = self.__check_proxy(proxy)
        self.folder_name = self.__check_folder_name(folder_name)
        self.name_format = self.__check_name_format(name_format)
        self.name_length = self.__check_name_length(name_length)
        self.work_path = self.__check_work_path(work_path)
        self.cookie = self.__check_cookie(cookie)
        self.cover = self.__check_cover(cover)
        self.music = self.check_bool(music, False)
        self.data_record = self.check_bool(data_record, False)
        self.chunk = self.__check_chunk(chunk)
        self.folder_mode = self.check_bool(folder_mode, False)
        self.author_archive = self.check_bool(author_archive, False)
        self.max_workers = self.__check_max_workers(max_workers)
        self.user_agent = user_agent

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
            "cookie": self.cookie,
            "cover": self.cover,
            "music": self.music,
            "data_record": self.data_record,
            "max_workers": self.max_workers,
            "folder_mode": self.folder_mode,
            "chunk": self.chunk,
            "user_agent": self.user_agent,
            "name_format": self.name_format,
            "name_length": self.name_length,
            "mapping_data": self.mapping_data,
            "author_archive": self.author_archive,
        }

    def __check_timeout(self, timeout: int) -> int:
        if not isinstance(timeout, int) or timeout <= 0:
            self.console.warning(_("timeout 参数错误"))
            return 10
        return timeout

    def __check_max_retry(self, max_retry: int) -> int:
        if not isinstance(max_retry, int) or max_retry < 0:
            self.console.warning(_("max_retry 参数错误"))
            return 5
        return max_retry

    def __check_max_workers(self, max_workers: int) -> int:
        if isinstance(max_workers, int) and max_workers > 0:
            return max_workers
        self.console.warning(_("max_workers 参数错误"))
        return 4

    def __check_proxy(
        self,
        proxy: str,
        url="https://www.kuaishou.com/new-reco",
    ) -> str | None:
        if proxy:
            try:
                response = get(
                    url,
                    proxy=proxy,
                    timeout=TIMEOUT,
                    headers={
                        "User-Agent": PC_USERAGENT,
                    },
                )
                response.raise_for_status()
                self.console.info(_("代理 {proxy} 测试成功").format(proxy=proxy))
                return proxy
            except TimeoutException:
                self.console.warning(_("代理 {proxy} 测试超时").format(proxy=proxy))
            except HTTPError as e:
                self.console.warning(
                    _("代理 {proxy} 测试失败：{error}").format(proxy=proxy, error=e)
                )

    def __check_work_path(self, work_path: str) -> Path:
        if not work_path:
            return self.root
        if (r := Path(work_path)).is_dir():
            return r
        if r := self.__check_root_again(r):
            return r
        self.console.warning(
            _(
                "work_path 参数不是有效的文件夹路径，程序将使用 项目根路径/Volume 作为储存路径"
            )
        )
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
        self.console.warning(
            _("folder_name 参数不是有效的文件夹名称，程序将使用默认值：Download")
        )
        return "Download"

    def __check_cookie(self, cookie: str | dict) -> str:
        if isinstance(cookie, str):
            return cookie
        # elif isinstance(cookie, dict):
        #     pass
        self.console.warning(_("cookie 参数错误"))
        return ""

    def __check_cover(self, cover: str) -> str:
        if (c := cover.upper()) in {"", "JPEG", "WEBP"}:
            return c
        self.console.warning(_("cover 参数错误"))
        return ""

    @staticmethod
    def check_bool(value: bool, default: bool) -> bool:
        return value if isinstance(value, bool) else default

    def __check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk >= 256 * 1024:
            return chunk
        self.console.warning("chunk 参数错误")
        return 2 * 1024 * 1024

    def __check_name_format(self, name_format: str) -> list[str]:
        default = ["发布日期", "作者昵称", "作品描述"]
        if not name_format:
            return default
        name_format = name_format.split()
        for i in name_format:
            if i not in self.NAME_KEYS:
                self.console.warning(
                    _("name_format 参数包含未知字段: {field}").format(field=i)
                )
                return default
        return name_format

    def __check_name_length(self, name_length: int) -> int:
        if not isinstance(name_length, int):
            self.console.warning(_("name_length 参数错误"))
            return 128
        if name_length >16:
            return name_length
        self.console.warning(_("name_length 参数过小"))
        return 128
