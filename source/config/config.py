from platform import system
from typing import TYPE_CHECKING
from shutil import move
from yaml import dump, safe_load

from ..static import PROJECT_ROOT
from ..translation import _
from ..variable import PC_USERAGENT, RETRY, TIMEOUT

if TYPE_CHECKING:
    from ..tools import ColorConsole


class Config:
    default = {
        "mapping_data": {
            "作者ID(AuthorID)": "作者别名(AuthorAlias)",
        },
        "work_path": "",
        "folder_name": "Download",
        "name_format": "发布日期 作者昵称 作品描述",
        "name_length": 128,
        "cookie": "",
        "proxy": None,
        "data_record": False,
        "max_workers": 4,
        "cover": "",
        "music": False,
        "max_retry": RETRY,
        "timeout": TIMEOUT,
        "chunk": 2 * 1024 * 1024,
        "user_agent": PC_USERAGENT,
        "folder_mode": False,
        "author_archive": False,
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
        self.compatible()
        if self.file.exists():
            try:
                with self.file.open("r", encoding=self.encode) as file:
                    self.data = self.supplement(safe_load(file))
            except UnicodeDecodeError as e:
                self.console.error(_("配置文件编码错误：{error}").format(error=e))
                self.console.warning(_("本次运作将会使用默认配置参数！"))
                self.data = self.default
        else:
            self.__create()
            self.data = self.default
        return self.data

    def __create(self):
        self.console.info(_("已创建默认配置文件"))
        self.write(self.default)

    def write(self, data: dict = None) -> None:
        with self.file.open("w", encoding=self.encode) as file:
            dump(
                data or self.data,
                file,
                default_flow_style=False,
                allow_unicode=True,
            )

    def compatible(self):
        if (
            (old := PROJECT_ROOT.parent.joinpath("config.yaml")).exists()
        ) and not self.file.exists():
            move(old, self.file)

    def supplement(self, data:dict,)->dict:
        update = False
        for key, value in self.default.items():
            if key not in data:
                data[key] = value
                update = True
        if update:
            self.write(data)
        return data
