from shutil import rmtree
from typing import TYPE_CHECKING

from source.tools import base_session
from source.variable import (
    APP_HEADERS,
    APP_DATA_HEADERS,
    APP_DOWNLOAD_HEADERS,
    PC_DATA_HEADERS,
    PC_PAGE_HEADERS,
)

if TYPE_CHECKING:
    from pathlib import Path
    from source.tools import ColorConsole
    from source.tools import Cleaner


class Manager:
    def __init__(self,
                 console: "ColorConsole",
                 cleaner: "Cleaner",
                 root: "Path",
                 timeout: int,
                 max_retry: int,
                 proxy: str | None,
                 work_path: "Path",
                 folder_name: str,
                 # cookie: str,
                 cover: str,
                 download_record: bool,
                 data_record: bool,
                 max_workers: int,
                 ):
        self.console = console
        self.cleaner = cleaner
        self.root = root
        self.path = work_path
        self.temp = self.root.joinpath("Temp")
        self.data = self.path.joinpath("Data")
        self.folder = self.root.joinpath(folder_name)
        self.timeout = timeout
        self.session = base_session(timeout=timeout)
        self.pc_headers = PC_PAGE_HEADERS
        self.pc_data_headers = PC_DATA_HEADERS
        self.pc_download_headers = None
        self.app_headers = APP_HEADERS
        self.app_data_headers = APP_DATA_HEADERS
        self.app_download_headers = APP_DOWNLOAD_HEADERS
        self.max_retry = max_retry
        self.proxy = proxy
        self.cover = cover
        self.download_record = download_record
        self.data_record = data_record
        self.max_workers = max_workers
        self.__create_folder()

    def __create_folder(self):
        self.temp.mkdir(exist_ok=True)
        self.data.mkdir(exist_ok=True)
        self.folder.mkdir(exist_ok=True)

    def __clear_temp(self):
        rmtree(self.temp.resolve())

    async def close(self):
        await self.session.close()
        self.__clear_temp()
