from typing import TYPE_CHECKING

from yaml import dump
from yaml import safe_load

from source.custom import PROJECT_ROOT
from source.variable import RETRY
from source.variable import TIMEOUT

if TYPE_CHECKING:
    from source.tools import ColorConsole


class Config:
    default = {
        "work_path": "",
        "folder_name": "Download",
        "proxy": None,
        "download_record": True,
        "data_record": False,
        "max_workers": 4,
        "cover": "",
        "music": False,
        "max_retry": RETRY,
        "timeout": TIMEOUT,
        "chunk": 1024 * 1024,
        "folder_mode": False,
        # "cookie": "",
    }

    def __init__(self, console: "ColorConsole", ):
        self.console = console
        self.file = PROJECT_ROOT.joinpath("config.yaml")
        self.data = {}

    def read(self) -> dict:
        if self.file.exists():
            with self.file.open('r') as file:
                self.data = safe_load(file)
        else:
            self.__create()
            self.data = self.default
        return self.data

    def __create(self):
        self.console.info("已创建默认配置文件")
        self.write(self.default)

    def write(self, data: dict = None) -> None:
        with self.file.open('w') as file:
            dump(data or self.data, file, default_flow_style=False)
