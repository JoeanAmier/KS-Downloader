from source.config import Config
from source.config import Parameter
from source.custom import (
    PROJECT_NAME,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    DISCLAIMER_TEXT,
)
from source.downloader import Downloader
from source.extract import APIExtractor
from source.extract import PageExtractor
from source.link import DetailPage
from source.link import Examiner
from source.manager import Manager
from source.module import Database
from source.module import choose
from source.record import RecordManager
from source.request import Detail
from source.tools import Cleaner
from source.tools import (
    ColorConsole,
    ERROR,
    INFO,
    WARNING,
    MASTER,
)
from source.tools import Version


class KS:
    cleaner = Cleaner()

    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

    MENU_TIP = {
        0: "启用",
        1: "禁用",
    }

    def __init__(self):
        self.console = ColorConsole()
        self.config = Config(self.console)
        self.params = Parameter(
            console=self.console,
            cleaner=self.cleaner,
            **self.config.read(),
        )
        self.database = Database()
        self.config = None
        self.record = RecordManager()
        self.manager = Manager(**self.params.run())
        self.version = Version(self.manager)
        self.examiner = Examiner(self.manager)
        self.detail_request = Detail(self.manager)
        self.detail_page = DetailPage(self.manager)
        self.api_extractor = APIExtractor(self.manager)
        self.detail_extractor = PageExtractor(self.manager)
        self.download = Downloader(self.manager, self.database)
        self.running = True
        self.__function = None

    async def run(self):
        self.config = await self.database.read_config()
        self.__welcome()
        await self.__update_version()
        if await self.disclaimer():
            await self.__main_menu()

    async def __detail_enquire(self):
        while self.running:
            text = self.console.input("请输入快手作品链接：")
            if not text:
                break
            if text.upper() == "Q":
                self.running = False
                break
            await self.detail(text)

    async def __main_menu(self):
        while self.running:
            self.__update_menu()
            function = choose(
                "请选择 KS-Downloader 功能",
                [i for i, _ in self.__function],
                self.console,
            )
            if function.upper() == "Q":
                self.running = False
            try:
                n = int(function) - 1
            except ValueError:
                break
            if n in range(len(self.__function)):
                await self.__function[n][1]()

    def __update_menu(self):
        self.__function = (
            ("批量下载快手作品", self.__detail_enquire),
            (f"{self.MENU_TIP[self.config["Update"]]}检查更新功能", self.__modify_update),
            (f"{self.MENU_TIP[self.config["Record"]]}下载记录功能", self.__modify_record),
        )

    async def __update_version(self):
        if not self.config["Update"]:
            return
        if target := await self.version.get_target_version():
            state = self.version.compare_versions(
                f"{VERSION_MAJOR}.{VERSION_MINOR}", target, VERSION_BETA)
            self.console.print(
                self.version.STATUS_CODE[state],
                style=INFO if state == 1 else WARNING)
        else:
            self.console.print("检测新版本失败", style=ERROR)
        self.console.print()

    async def __modify_update(self):
        await self.__update_config("Update", 0 if self.config["Update"] else 1)

    async def __modify_record(self):
        await self.__update_config("Record", 0 if self.config["Record"] else 1)
        self.database.record = self.config["Record"]

    async def __update_config(self, key: str, value: int):
        self.config[key] = value
        await self.database.update_config_data(key, value)

    def __welcome(self):
        self.console.print(self.LINE, style=MASTER)
        self.console.print("\n")
        self.console.print(
            self.NAME.center(
                self.WIDTH),
            style=MASTER)
        self.console.print("\n")
        self.console.print(self.LINE, style=MASTER)
        self.console.print()

    async def detail(self, detail: str):
        app, urls = await self.examiner.run(detail)
        if not urls:
            return
        match app:
            case True:
                items = [await self.detail_request.run(i) for i in urls]
                data = self.api_extractor.run([i for i in items if i])
                data = self.__check_extract_data(data)
                await self.__save_data(data, "Download")
            case False:
                items = await self.detail_page.run(urls)
                data = [
                    self.detail_extractor.run(
                        h, i, ) for i, h in items if h]
                data = self.__check_extract_data(data)
            case _:
                return
        await self.__download_file(data, app=app, )

    async def __save_data(self, data: list[dict], name: str, type_="detail", format_="SQLite") -> None:
        if not data:
            return
        recorder, params = self.record.run(type_, format_)
        async with recorder(self.manager, db_name=name, **params) as record:
            for i in data:
                await record.update(i)

    async def __download_file(self, data: list[dict], type_="detail", app=True, ):
        if data:
            await self.download.run(data, type_, app, )

    def __check_extract_data(self, data: list) -> list:
        if data := [i for i in data if i]:
            return data
        self.console.error("获取作品数据失败")
        return []

    async def user(self):
        pass

    async def disclaimer(self):
        if self.config["Disclaimer"]:
            return True
        self.console.print(
            "\n".join(DISCLAIMER_TEXT),
            style=MASTER)
        if self.console.input(
                "是否已仔细阅读上述免责声明(YES/NO): ").upper() != "YES":
            return False
        await self.database.update_config_data("Disclaimer", 1)
        self.console.print()
        return True

    async def close(self):
        await self.manager.close()

    async def __aenter__(self):
        await self.database.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.database.__aexit__(exc_type, exc_val, exc_tb)
        await self.close()
