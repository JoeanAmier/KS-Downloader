from source.config import Config
from source.config import Parameter
from source.downloader import Downloader
from source.extract import APIExtractor
from source.extract import HTMLExtractor
from source.link import DetailPage
from source.link import Examiner
from source.manager import Manager
from source.module import Database
from source.module import choose
from source.record import RecordManager
from source.request import Detail
from source.static import (
    PROJECT_NAME,
    VERSION_MAJOR,
    VERSION_MINOR,
    VERSION_BETA,
    DISCLAIMER_TEXT,
    REPOSITORY,
    LICENCE,
)
from source.tools import BrowserCookie
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
    VERSION_MAJOR = VERSION_MAJOR
    VERSION_MINOR = VERSION_MINOR
    VERSION_BETA = VERSION_BETA

    cleaner = Cleaner()

    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

    MENU_TIP = {
        0: "启用",
        1: "禁用",
    }

    DOMAINS: list[str] = [
        # "chenzhongtech.com",
        "kuaishou.com",
        # "kuaishou.cn",
    ]

    def __init__(self):
        self.console = ColorConsole()
        self.config_obj = Config(self.console)
        self.params = Parameter(
            console=self.console,
            cleaner=self.cleaner,
            **self.config_obj.read(),
        )
        self.database = Database()
        self.config = None
        self.record = RecordManager()
        self.manager = Manager(**self.params.run())
        self.version = Version(self.manager)
        self.examiner = Examiner(self.manager)
        self.detail_html = DetailPage(self.manager)
        self.extractor_api = APIExtractor(self.manager)
        self.extractor_html = HTMLExtractor(self.manager)
        self.download = Downloader(self.manager, self.database)
        self.running = True
        self.__function = None

    async def run(self):
        self.config = await self.database.read_config()
        self.__welcome()
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

    async def __read_cookie(self):
        if c := BrowserCookie.run(self.DOMAINS, self.console, ):
            self.config_obj.write(self.config_obj.read() | {"cookie": c})
            self.console.print("读取并写入 Cookie 成功！", style=INFO)

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
            ("从浏览器读取 Cookie", self.__read_cookie),
            ("批量下载快手作品", self.__detail_enquire),
            (f"{self.MENU_TIP[self.config["Record"]]}下载记录功能", self.__modify_record),
            ("检查程序版本更新", self.__update_version),
        )

    async def __update_version(self):
        if target := await self.version.get_target_version():
            state = self.version.compare_versions(
                f"{self.VERSION_MAJOR}.{self.VERSION_MINOR}",
                target,
                self.VERSION_BETA,
            )
            self.console.print(
                self.version.STATUS_CODE[state],
                style=INFO if state == 1 else WARNING)
        else:
            self.console.print("检测新版本失败", style=ERROR)

    async def __modify_record(self):
        await self.__update_config("Record", 0 if self.config["Record"] else 1)
        self.database.record = self.config["Record"]
        self.console.print("修改设置成功！", style=INFO, )

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
        self.console.print(f"项目地址：{REPOSITORY}", style=MASTER)
        self.console.print(f"开源协议：{LICENCE}", style=MASTER)
        self.console.print()

    async def detail(self, detail: str):
        urls = await self.examiner.run(detail)
        if not urls:
            self.console.warning("提取作品链接失败")
            return
        for url in urls:
            web, user_id, detail_id = self.examiner.extract_params(url, )
            if not detail_id:
                self.console.warning(f"URL 解析失败：{url}")
                continue
            data = await self.__handle_detail_html(
                detail_id,
                url,
                web,
            )
            if not any(data):
                continue
            await self.__download_file(data, )
            await self.__save_data(data, "Download")

    async def __handle_detail_api(
            self,
            user_id: str,
            detail_id: str,
    ):
        data = await Detail(
            self.manager,
            user_id,
            detail_id,
        ).run()
        data = self.extractor_api.run([data])
        # await self.__save_data(data, "Download")
        return data

    async def __handle_detail_html(
            self,
            detail_id: str,
            url: str,
            web: bool,
    ) -> list[dict]:
        if html := await self.detail_html.run(url):
            return [self.extractor_html.run(html, detail_id, web, )]

    async def __save_data(self, data: list[dict], name: str, type_="detail", format_="SQLite") -> None:
        recorder, params = self.record.run(type_, format_)
        async with recorder(self.manager, db_name=name, **params) as record:
            for i in data:
                i["download"] = " ".join(i["download"])
                await record.update(i)

    async def __download_file(self, data: list[dict], type_="detail", ):
        await self.download.run(data, type_, )

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
