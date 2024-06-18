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
                 cleaner: "Cleaner",
                 cookie: str = "kpf=PC_WEB; clientid=3; did=web_eda1a93f1f2a99778b3dea2ed60fc496; arp_scroll_position=0; userId=3568785353; kpn=KUAISHOU_VISION; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABudUVe1aunIWZSj6PE3uzs67cNzH-u5iyM44cD-NrZMfYX3CxZhlerbs70kawwFNxwO_THqC0Nf4gJX8NLg72iiXDKhf2WyPRNrL-JplI6wpbEMT_hQld8muKZD679iFrkGtXHiCA4391rkmAE2COAE8E2wf6_mY43fH7Ccbbaqks3K1hBdx62P-xvWbRjj0714LEf09TPgN-W8BkJeNdgxoStEyT9S95saEmiR8Dg-bb1DKRIiBsiinsiplsExnD2Hh-ZL1z_pdtWpKi_aIQWjmGfN17MigFMAE; kuaishou.server.web_ph=ad0f7ffe552ff2aa87ae7270235d15d81d32",
                 folder_name: str = "Download",
                 work_path: str = "",
                 timeout=TIMEOUT,
                 max_retry=RETRY,
                 proxy: str = None,
                 cover="",
                 music=False,
                 download_record: bool = True,
                 data_record: bool = False,
                 chunk=1024 * 1024,
                 folder_mode: bool = False,
                 max_workers=4,
                 ):
        self.root = PROJECT_ROOT
        self.cleaner = cleaner
        self.console = console
        self.timeout = self.__check_timeout(timeout)
        self.retry = self.__check_max_retry(max_retry)
        self.proxy = proxy
        self.folder_name = self.__check_folder_name(folder_name)
        self.work_path = self.__check_work_path(work_path)
        self.cookie = self.__check_cookie(cookie)
        self.cover = self.__check_cover(cover)
        self.music = self.check_bool(music, False)
        self.download_record = self.check_bool(download_record, True)
        self.data_record = self.check_bool(data_record, False)
        self.chunk = self.__check_chunk(chunk)
        self.folder_mode = self.check_bool(folder_mode, False)
        self.max_workers = self.__check_max_workers(max_workers)

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
            "download_record": self.download_record,
            "data_record": self.data_record,
            "max_workers": self.max_workers,
            "folder_mode": self.folder_mode,
            "chunk": self.chunk,
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
        self.proxy = await self.__check_proxy(self.proxy) if self.proxy else None

    def __check_max_workers(self, max_workers: int) -> int:
        if isinstance(max_workers, int) and max_workers > 0:
            return max_workers
        self.console.warning("max_workers 参数错误")
        return 4

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

    @staticmethod
    def check_bool(value: bool, default: bool) -> bool:
        return value if isinstance(value, bool) else default

    def __check_chunk(self, chunk: int) -> int:
        if isinstance(chunk, int) and chunk > 1024:
            return chunk
        self.console.warning("chunk 参数错误")
        return 1024 * 1024
