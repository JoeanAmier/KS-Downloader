from uvicorn import Config as APIConfig
from uvicorn import Server
from source.config import Config, Parameter
from source.downloader import Downloader
from source.extract import APIExtractor, HTMLExtractor
from source.link import DetailPage, Examiner
from source.manager import Manager
from source.module import Database, choose
from source.record import RecordManager
from source.request import Detail
from source.static import (
    DISCLAIMER_TEXT,
    LICENCE,
    PROJECT_NAME,
    REPOSITORY,
    VERSION_BETA,
    VERSION_MAJOR,
    VERSION_MINOR,
    __VERSION__,
)
from source.tools import (
    ERROR,
    INFO,
    MASTER,
    WARNING,
    BrowserCookie,
    Cleaner,
    ColorConsole,
    Mapping,
    Version,
)
from source.translation import _, switch_language
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from source.model import (
    DetailModel,
    ResponseModel,
    ShortUrl,
    UrlResponse,
)


class KS:
    VERSION_MAJOR = VERSION_MAJOR
    VERSION_MINOR = VERSION_MINOR
    VERSION_BETA = VERSION_BETA

    cleaner = Cleaner()

    NAME = PROJECT_NAME
    WIDTH = 50
    LINE = ">" * WIDTH

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
        self.config = None
        self.option = None
        self.record = RecordManager()
        self.manager = Manager(**self.params.run())
        self.database = Database(self.manager)
        self.mapping = Mapping(self.manager, self.database)
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
        self.option = await self.database.read_option()
        self.set_language(self.option["Language"])
        self.__welcome()
        if await self.disclaimer():
            await self.__main_menu()

    async def __detail_enquire(self):
        while self.running:
            text = self.console.input(_("请输入快手作品链接："))
            if not text:
                break
            if text.upper() == "Q":
                self.running = False
                break
            await self.detail(text)

    async def __read_cookie(self):
        if c := BrowserCookie.run(
            self.DOMAINS,
            self.console,
        ):
            self.config_obj.write(self.config_obj.read() | {"cookie": c})
            self.console.print(_("读取并写入 Cookie 成功！"), style=INFO)

    async def __main_menu(self):
        while self.running:
            self.__update_menu()
            function = choose(
                _("请选择 KS-Downloader 功能"),
                [i for i, __ in self.__function],
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
        tip = {
            0: _("启用"),
            1: _("禁用"),
        }
        self.__function = (
            (_("从浏览器读取 Cookie"), self.__read_cookie),
            (_("批量下载链接作品"), self.__detail_enquire),
            (
                tip[self.config["Record"]] + _("下载记录功能"),
                self.__modify_record,
            ),
            (_("检查程序版本更新"), self.__update_version),
            (_("切换语言"), self._switch_language),
        )

    async def _switch_language(
        self,
    ):
        if self.option["Language"] == "zh_CN":
            language = "en_US"
        elif self.option["Language"] == "en_US":
            language = "zh_CN"
        else:
            raise TypeError(self.option["Language"])
        await self._update_language(language)

    async def __update_version(self):
        if target := await self.version.get_target_version():
            state = self.version.compare_versions(
                f"{self.VERSION_MAJOR}.{self.VERSION_MINOR}",
                target,
                self.VERSION_BETA,
            )
            self.console.print(
                self.version.STATUS_CODE[state], style=INFO if state == 1 else WARNING
            )
        else:
            self.console.print(_("检测新版本失败"), style=ERROR)

    async def __modify_record(self):
        await self.__update_config("Record", 0 if self.config["Record"] else 1)
        self.database.record = self.config["Record"]
        self.console.print(
            _("修改设置成功！"),
            style=INFO,
        )

    async def __update_config(self, key: str, value: int):
        self.config[key] = value
        await self.database.update_config_data(key, value)

    def __welcome(self):
        self.console.print(self.LINE, style=MASTER)
        self.console.print("\n")
        self.console.print(self.NAME.center(self.WIDTH), style=MASTER)
        self.console.print("\n")
        self.console.print(self.LINE, style=MASTER)
        self.console.print()
        self.console.print(_("项目地址：{repo}").format(repo=REPOSITORY), style=MASTER)
        self.console.print(
            _("开源协议：{licence}").format(licence=LICENCE), style=MASTER
        )
        self.console.print()

    async def detail(
        self,
        detail: str,
        download: bool = True,
    ):
        urls = await self.examiner.run(
            detail,
        )
        if not urls:
            message = _("提取作品链接失败")
            self.console.warning(message)
            return message
        for url in urls:
            await self.detail_one(
                url,
                download,
            )

    async def detail_one(
        self,
        url: str,
        download: bool = False,
        proxy: str = "",
        cookie: str = "",
    ) -> dict | str:
        web, user_id, detail_id = self.examiner.extract_params(
            url,
        )
        if not detail_id:
            message = _("URL 解析失败：{url}").format(url=url)
            self.console.warning(message)
            return message
        data = await self.__handle_detail_html(
            detail_id,
            url,
            web,
            proxy,
            cookie,
        )
        if not data:
            return _("获取作品数据失败")
        await self.update_author_nickname(
            data,
        )
        if download:
            await self.__download_file(
                [data],
            )
        await self.__save_data([data], "Download")
        return data

    async def update_author_nickname(
        self,
        data: dict,
    ):
        if a := self.cleaner.filter_name(
            self.manager.mapping_data.get(i := data["authorID"], "")
        ):
            data["name"] = a
        else:
            data["name"] = self.manager.filter_name(data["name"]) or i
        await self.mapping.update_cache(
            i,
            data["name"],
        )

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
        proxy: str = "",
        cookie: str = "",
    ) -> dict | None:
        if html := await self.detail_html.run(url, proxy, cookie):
            return self.extractor_html.run(
                html,
                detail_id,
                web,
            )
        return None

    async def __save_data(
        self, data: list[dict], name: str, type_="detail", format_="SQLite"
    ) -> None:
        recorder, params = self.record.run(type_, format_)
        async with recorder(self.manager, db_name=name, **params) as record:
            for i in data:
                i["download"] = " ".join(i["download"])
                await record.update(i)

    async def __download_file(
        self,
        data: list[dict],
        type_="detail",
    ):
        await self.download.run(
            data,
            type_,
        )

    async def user(self):
        pass

    async def disclaimer(self):
        if self.config["Disclaimer"]:
            return True
        await self.__init_language()
        self.console.print(
            _(DISCLAIMER_TEXT),
            style=MASTER,
        )
        if self.console.input(
            _("是否已仔细阅读上述免责声明(YES/NO): ")
        ).upper() not in (
            "YES",
            "Y",
        ):
            return False
        await self.database.update_config_data("Disclaimer", 1)
        self.console.print()
        return True

    async def __init_language(self):
        languages = (
            (
                "简体中文",
                "zh_CN",
            ),
            (
                "English",
                "en_US",
            ),
        )
        language = choose(
            "请选择语言(Please Select Language)",
            [i[0] for i in languages],
            self.console,
        )
        try:
            language = languages[int(language) - 1][1]
            await self._update_language(language)
        except ValueError:
            await self.__init_language()

    async def _update_language(self, language: str) -> None:
        self.option["Language"] = language
        await self.database.update_option_data("Language", language)
        self.set_language(language)

    async def close(self):
        await self.manager.close()

    async def __aenter__(self):
        await self.database.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.database.__aexit__(exc_type, exc_val, exc_tb)
        await self.close()

    @staticmethod
    def set_language(language: str) -> None:
        switch_language(language)

    async def run_server(
        self,
        host="0.0.0.0",
        port=5556,
        log_level="info",
    ):
        self.server = FastAPI(
            debug=self.VERSION_BETA,
            title="KS-Downloader",
            version=__VERSION__,
        )
        self.setup_routes()
        config = APIConfig(
            self.server,
            host=host,
            port=port,
            log_level=log_level,
        )
        server = Server(config)
        await server.serve()

    def setup_routes(self):
        @self.server.get("/")
        async def index():
            return RedirectResponse(url=REPOSITORY)

        @self.server.post(
            "/share",
            response_model=UrlResponse,
        )
        async def share(extract: ShortUrl):
            if urls := await self.examiner.run(
                extract.text,
                type_="",
                proxy=extract.proxy,
            ):
                return UrlResponse(
                    message=_("请求重定向链接成功！"),
                    params=extract,
                    urls=urls,
                )
            return UrlResponse(
                message=_("请求重定向链接失败！"),
                params=extract,
                urls=None,
            )

        @self.server.post(
            "/detail/",
            response_model=ResponseModel,
        )
        async def detail(extract: DetailModel):
            urls = await self.examiner.run(extract.text, proxy=extract.proxy)
            if not urls:
                message = _("提取作品链接失败")
                data = None
                self.console.warning(message)
            else:
                if isinstance(
                    data := await self.detail_one(
                        urls[0], proxy=extract.proxy, cookie=extract.cookie
                    ),
                    dict,
                ):
                    message = _("获取作品数据成功")
                else:
                    message = data
                    data = None
            return ResponseModel(message=message, params=extract, data=data)
