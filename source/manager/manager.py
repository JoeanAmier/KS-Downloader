from shutil import rmtree
from typing import TYPE_CHECKING

from ..tools import base_client
from ..tools import remove_empty_directories
from ..variable import (
    APP_HEADERS,
    APP_DATA_HEADERS,
    APP_DOWNLOAD_HEADERS,
    PC_DATA_HEADERS,
    PC_PAGE_HEADERS,
    PC_DOWNLOAD_HEADERS,
)

if TYPE_CHECKING:
    from pathlib import Path
    from ..tools import ColorConsole
    from ..tools import Cleaner


class Manager:
    def __init__(self,
                 console: "ColorConsole",
                 cleaner: "Cleaner",
                 root: "Path",
                 timeout: int,
                 max_retry: int,
                 proxy: dict,
                 work_path: "Path",
                 folder_name: str,
                 name_format: str,
                 cookie: str,
                 cover: str,
                 music: bool,
                 data_record: bool,
                 chunk: int,
                 folder_mode: bool,
                 max_workers: int,
                 *args,
                 **kwargs,
                 ):
        self.console = console
        self.cleaner = cleaner
        self.root = root
        self.path = work_path
        self.temp = self.root.joinpath("Temp")
        self.data = self.path.joinpath("Data")
        self.folder = self.root.joinpath(folder_name)
        self.timeout = timeout
        self.client = base_client(timeout=timeout, proxy=proxy, )
        self.cookie = cookie
        self.pc_headers = PC_PAGE_HEADERS | {"Cookie": cookie}
        self.pc_data_headers = PC_DATA_HEADERS | {"Cookie": cookie}
        self.pc_download_headers = PC_DOWNLOAD_HEADERS
        self.app_headers = APP_HEADERS | {"Cookie": cookie}
        self.app_data_headers = APP_DATA_HEADERS | {"Cookie": cookie}
        self.app_download_headers = APP_DOWNLOAD_HEADERS
        self.name_format = name_format
        self.max_retry = max_retry
        self.proxy = proxy
        self.cover = cover
        self.music = music
        self.data_record = data_record
        self.folder_mode = folder_mode
        self.chunk = chunk
        self.max_workers = max_workers
        self.__create_folder()

    def __create_folder(self):
        self.temp.mkdir(exist_ok=True)
        self.data.mkdir(exist_ok=True)
        self.folder.mkdir(exist_ok=True)

    def __clear_temp(self):
        rmtree(self.temp.resolve())

    async def close(self):
        await self.client.aclose()
        # self.__clear_temp()
        remove_empty_directories(self.root)
