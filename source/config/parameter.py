from pathlib import Path
from typing import TYPE_CHECKING

from curl_cffi.requests import get
from curl_cffi.requests.exceptions import RequestException, Timeout
from typing import get_args
from curl_cffi.requests import BrowserTypeLiteral
from ..static import PROJECT_ROOT
from ..translation import _
from ..variable import PC_IMPERSONATE, RETRY, TIMEOUT
from ..tools import cookie_str_to_dict

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
        cookies: str | dict,
        folder_name: str = "Download",
        name_format: str = "发布日期 作者昵称 作品描述",
        name_length: int = 128,
        work_path: str = "",
        timeout=TIMEOUT,
        max_retry=RETRY,
        proxy: str | None = None,
        download_cover="",
        download_music=False,
        data_record: bool = False,
        download_chunk=1024 * 1024,
        impersonate=PC_IMPERSONATE,
        folder_mode: bool = False,
        author_archive: bool = False,
        max_workers=4,
        **kwargs,
    ):
        self.root = PROJECT_ROOT
        self.cleaner = cleaner
        self.console = console
        self.mapping_data = mapping_data or {}
        self.timeout = self.__check_timeout(timeout)
        self.max_retry = self.__check_max_retry(max_retry)
        self.proxy = self.__check_proxy(proxy)
        self.folder_name = self.__check_folder_name(folder_name)
        self.name_format = self.__check_name_format(name_format)
        self.name_length = self.__check_name_length(name_length)
        self.work_path = self.__check_work_path(work_path)
        self.cookies = self.__check_cookies(cookies)
        self.download_cover = self.__check_download_cover(download_cover)
        self.download_music = self.check_bool("download_music", download_music, False)
        self.data_record = self.check_bool("data_record", data_record, False)
        self.download_chunk = self.__check_download_chunk(download_chunk)
        self.folder_mode = self.check_bool("folder_mode", folder_mode, False)
        self.author_archive = self.check_bool("author_archive", author_archive, False)
        self.max_workers = self.__check_max_workers(max_workers)
        self.impersonate = self.__check_impersonate(impersonate)

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
        proxy: str | None,
        url="https://www.kuaishou.com/new-reco",
    ) -> str | None:
        if proxy:
            try:
                response = get(
                    url,
                    proxy=proxy,
                    timeout=TIMEOUT,
                    impersonate=PC_IMPERSONATE,
                )
                response.raise_for_status()
                self.console.info(_("代理 {proxy} 测试成功").format(proxy=proxy))
                return proxy
            except Timeout:
                self.console.warning(_("代理 {proxy} 测试超时").format(proxy=proxy))
            except RequestException as e:
                self.console.warning(
                    _("代理 {proxy} 测试失败：{error}").format(proxy=proxy, error=e)
                )
        return None

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

    def __check_cookies(self, cookie: str | dict) -> dict:
        if isinstance(cookie, str):
            return cookie_str_to_dict(cookie)
        elif isinstance(cookie, dict):
            return cookie
        self.console.warning(_("cookies 参数错误"))
        return {}

    def __check_download_cover(self, cover: str) -> str:
        if (c := cover.upper()) in {"", "JPEG", "WEBP"}:
            return c
        self.console.warning(_("download_cover 参数错误"))
        return ""

    def check_bool(self, name: str, value: bool, default: bool) -> bool:
        if not isinstance(value, bool):
            self.console.warning(
                _("参数 {name} 错误，使用默认值: {default}").format(
                    name=name, default=default
                )
            )
            return default
        return value

    def __check_download_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk >= 256 * 1024:
            return chunk
        self.console.warning(_("download_chunk 参数错误"))
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
        if name_length > 16:
            return name_length
        self.console.warning(_("name_length 参数过小"))
        return 128

    def __check_impersonate(self, impersonate: str) -> str:
        impersonate_values = list(get_args(BrowserTypeLiteral))
        if impersonate in impersonate_values:
            return impersonate
        self.console.warning(_("impersonate 参数无效"))
        return PC_IMPERSONATE
