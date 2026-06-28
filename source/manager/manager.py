from re import compile, sub
from shutil import rmtree, move
from typing import TYPE_CHECKING

from ..tools import base_client, remove_empty_directories
from ..variable import (
    PC_PAGE_HEADERS,
)

if TYPE_CHECKING:
    from pathlib import Path

    from ..tools import Cleaner, ColorConsole


class Manager:
    NAME = compile(r"[^\u4e00-\u9fffa-zA-Z0-9-_！？，。；：“”（）《》]")

    def __init__(
        self,
        console: "ColorConsole",
        cleaner: "Cleaner",
        root: "Path",
        mapping_data: dict,
        timeout: int,
        max_retry: int,
        proxy: dict,
        work_path: "Path",
        folder_name: str,
        name_format: str,
        name_length: int,
        cookies: dict,
        download_cover: str,
        download_music: bool,
        data_record: bool,
        download_chunk: int,
        impersonate: str,
        folder_mode: bool,
        author_archive: bool,
        max_workers: int,
        **kwargs,
    ):
        self.console = console
        self.cleaner = cleaner
        self.root = root
        self.path = work_path
        self.temp = self.root.joinpath("Temp")
        self.data = self.path.joinpath("Data")
        self.folder = self.path.joinpath(folder_name)
        self.compatible(folder_name)
        self.timeout = timeout
        self.cookies = cookies
        self.impersonate = impersonate
        self.client = base_client(
            impersonate=impersonate,
            timeout=timeout,
            proxy=proxy,
            cookies=cookies,
            headers=PC_PAGE_HEADERS,
        )
        self.client_download = base_client(
            impersonate=impersonate,
            timeout=timeout,
            proxy=proxy,
        )
        self.name_format = name_format
        self.name_length = name_length
        self.max_retry = max_retry
        self.proxy = proxy
        self.download_cover = download_cover
        self.download_music = download_music
        self.data_record = data_record
        self.folder_mode = folder_mode
        self.author_archive = author_archive
        self.download_chunk = download_chunk
        self.mapping_data = mapping_data
        self.max_workers = max_workers
        self.__create_folder()

    def __create_folder(self):
        self.temp.mkdir(exist_ok=True)
        self.data.mkdir(exist_ok=True)
        self.folder.mkdir(exist_ok=True)

    def __clear_temp(self):
        rmtree(self.temp.resolve())

    def filter_name(self, name: str) -> str:
        name = self.NAME.sub("_", name)
        return sub(r"_+", "_", name).strip("_")

    async def close(self):
        await self.client.close()
        await self.client_download.close()
        # self.__clear_temp()
        remove_empty_directories(self.root)

    def compatible(self, folder_name: str):
        if (
            (old := self.root.parent.joinpath("Temp")).exists()
        ) and not self.temp.exists():
            move(old, self.temp)
        if (
            self.path == self.root
            and (old := self.path.parent.joinpath("Data")).exists()
            and not self.data.exists()
        ):
            move(old, self.data)
        if (
            self.path == self.root
            and (old := self.path.parent.joinpath(folder_name)).exists()
            and not self.folder.exists()
        ):
            move(old, self.folder)
