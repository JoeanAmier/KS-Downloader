from source.config import Config
from source.config import Parameter
from source.custom import PROJECT_NAME
from source.downloader import Downloader
from source.extract import APIExtractor
from source.link import Examiner
from source.manager import Manager
from source.record import RecordManager
from source.request import Detail
from source.tools import Cleaner
from source.tools import ColorConsole


class KS:
    cleaner = Cleaner()

    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

    def __init__(self):
        self.console = ColorConsole()
        self.config = Config(self.console)
        self.params = Parameter(
            console=self.console,
            cleaner=self.cleaner,
            **self.config.read(),
        )
        self.record = RecordManager()
        self.manager = Manager(**self.params.run())
        self.examiner = Examiner(self.manager)
        self.detail_request = Detail(self.manager)
        self.api_extractor = APIExtractor(self.manager)
        self.download = Downloader(self.manager)
        self.running = True

    async def async_init(self):
        await self.params.check_proxy()
        self.manager = Manager(**self.params.run())
        self.examiner = Examiner(self.manager)
        self.detail_request = Detail(self.manager)
        self.api_extractor = APIExtractor(self.manager)
        self.download = Downloader(self.manager)

    async def run(self):
        self.__welcome()
        # await self.async_init()
        while self.running:
            if not (text := self.console.input("请输入快手作品链接：")):
                # self.running = False
                # continue
                break
            # video = "https://v.kuaishou.com/sOky3y"
            # image = "https://v.kuaishou.com/w7CObm"
            # image = "https://v.kuaishou.com/sYuTcs"
            await self.detail(text)

    def __welcome(self):
        self.console.print(self.LINE, style=ColorConsole.MASTER)
        self.console.print("\n\n")
        self.console.print(
            self.NAME.center(
                self.WIDTH),
            style=ColorConsole.MASTER)
        self.console.print("\n\n")
        self.console.print(self.LINE, style=ColorConsole.MASTER)

    async def detail(self, detail: str):
        if not (urls := await self.examiner.run(detail)):
            self.console.warning("提取作品链接失败")
            return
        items = [await self.detail_request.run(i) for i in urls]
        data = self.api_extractor.run(items)
        await self.__save_data(data, "Download")
        await self.__download_file(data)

    async def __save_data(self, data: list[dict], name: str, type_="detail", format_="SQLite"):
        recorder, params = self.record.run(type_, format_)
        async with recorder(self.manager, db_name=name, **params) as record:
            for i in data:
                await record.update(i)

    async def __download_file(self, data: list[dict], type_="detail", ):
        await self.download.run(data, type_)

    async def user(self):
        pass

    async def close(self):
        await self.manager.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
