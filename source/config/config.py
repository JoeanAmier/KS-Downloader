from platform import system
from typing import TYPE_CHECKING

from yaml import dump
from yaml import safe_load

from ..static import PROJECT_ROOT
from ..variable import RETRY
from ..variable import TIMEOUT

if TYPE_CHECKING:
    from ..tools import ColorConsole


class Config:
    default = {
        "work_path": "",
        "folder_name": "Download",
        "name_format": "发布日期 作者昵称 作品描述",
        "cookie": "",
        "proxy": None,
        "data_record": False,
        "max_workers": 4,
        "cover": "",
        "music": False,
        "max_retry": RETRY,
        "timeout": TIMEOUT,
        "chunk": 2 * 1024 * 1024,
        # "user_agent": "",
        "folder_mode": False,
    }
    encode = "UTF-8-SIG" if system() == "Windows" else "UTF-8"

    def __init__(
            self,
            console: "ColorConsole",
    ):
        self.console = console
        self.file = PROJECT_ROOT.joinpath("config.yaml")
        self.data = {}

    def read(self) -> dict:
        if self.file.exists():
            try:
                with self.file.open("r", encoding=self.encode) as file:
                    self.data = safe_load(file)
            except UnicodeDecodeError as e:
                self.console.error(f"配置文件编码错误: {e}")
                self.console.warning("本次运作将会使用默认配置参数！")
                self.data = self.default
        else:
            self.__create()
            self.data = self.default
        return self.data

    def __create(self):
        self.console.info("已创建默认配置文件")
        self.write(self.default)

    def write(self, data: dict = None) -> None:
        with self.file.open("w", encoding=self.encode) as file:
            dump(
                data or self.data,
                file,
                default_flow_style=False,
                allow_unicode=True,
            )
