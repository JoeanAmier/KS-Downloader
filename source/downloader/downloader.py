from asyncio import gather
from shutil import move
from typing import TYPE_CHECKING

from rich.progress import (
    SpinnerColumn,
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from source.tools import ColorConsole
from source.tools import capture_error_request
from source.tools import retry_request

if TYPE_CHECKING:
    from source.manager import Manager
    from pathlib import Path


class Downloader:
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
    }

    def __init__(self, manager: "Manager"):
        self.path = manager.path
        self.folder = manager.folder
        self.session = manager.session
        self.headers = manager.app_download_headers
        self.cleaner = manager.cleaner
        self.cover = manager.cover
        self.console = manager.console
        self.proxy = manager.proxy
        self.retry = manager.max_retry
        self.temp = manager.temp
        self.chunk = 1024 * 1024

    def __general_progress_object(self) -> Progress:
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=ColorConsole.PROGRESS,
                justify="left"),
            SpinnerColumn(),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(
                binary_units=True),
            "•",
            TimeRemainingColumn(),
            console=self.console,
            transient=False,
            expand=True,
        )

    async def run(self, data: list[dict], type_="detail", ):
        match type_:
            case "detail":
                await self.__handle_detail(data)
            case "user":
                pass
            case _:
                raise ValueError

    async def __handle_detail(self, data: list[dict]):
        tasks = []
        with self.__general_progress_object() as progress:
            for item in data:
                name = self.__generate_name(item)
                match item["photoType"]:
                    case "视频":
                        await self.__handle_video(tasks, name, item, progress, )
                    case "图片":
                        await self.__handle_atlas(tasks, name, item["download"], progress, )
                    case _:
                        self.console.error("未知的作品类型")
            await gather(*tasks)

    async def __handle_video(self, tasks: list, name: str, data: dict, progress: Progress, ):
        file = self.folder.joinpath(name)
        if not self.__file_exists(file, "mp4"):
            tasks.append(
                self.__download_file(data["download"], file, progress, "视频", )
            )
        await self.__handle_cover(tasks, file, data, progress, )

    async def __handle_atlas(self, tasks: list, name: str, urls: str, progress: Progress, ):
        urls = urls.split()
        for index, url in enumerate(urls, start=1):
            file = self.folder.joinpath(f"{name}_{index}")
            if not self.__file_exists(file, ):
                tasks.append(
                    self.__download_file(url, file, progress, "图片", )
                )

    async def __handle_cover(self, tasks: list, path: "Path", data: dict, progress: Progress, ):
        match self.cover:
            case "WEBP":
                if not self.__file_exists(path, "webp"):
                    tasks.append(
                        self.__download_file(data["webpCoverUrls"], path, progress, "封面", )
                    )
            case "JPEG":
                if not self.__file_exists(path, "jpeg"):
                    tasks.append(
                        self.__download_file(data["coverUrls"], path, progress, "封面", )
                    )
            case "":
                pass

    @retry_request
    @capture_error_request
    async def __download_file(self, url: str, path: "Path", progress: Progress, tip: str = ""):
        if not url:
            self.console.warning(f"{path.name} {tip} 下载链接为空")
            return True
        async with self.session.get(url, headers=self.headers, proxy=self.proxy, ) as response:
            if response.status != 200:
                self.console.error(f"{path.name} 响应码异常：{response.status}")
                return False
            temp = self.temp.joinpath(path.name)
            suffix = self.__extract_type(response.headers.get("Content-Type"))
            path = path.with_name(f"{path.name}.{suffix}")
            task_id = progress.add_task(
                path.name, total=int(response.headers.get("Content-Length", "0")) or None)
            with temp.open("wb") as f:
                async for chunk in response.content.iter_chunked(self.chunk):
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
        self.move(temp, path)
        self.console.info(f"{path.name} 下载完成")
        return True

    @classmethod
    def __extract_type(cls, content: str) -> str:
        return cls.CONTENT_TYPE_MAP.get(content, "")

    @staticmethod
    def move(temp: "Path", path: "Path"):
        move(temp.resolve(), path.resolve())

    def __file_exists(self, path: "Path", suffix="*") -> bool:
        if e := any(path.parent.glob(n := f"{path.name}.{suffix}")):
            self.console.info(f"{n} 已存在，跳过下载")
        return e

    def __generate_path(self):
        pass

    def __generate_name(self, data: dict) -> str:
        type_ = data["photoType"]
        date = data["timestamp"].replace(":", ".")
        author = self.cleaner.filter_name(data["userName"]) or data["userEid"]
        caption = self.cleaner.filter_name(
            self.cleaner.clear_spaces(
                data["caption"])) or data["detailID"]
        return f"{type_}-{date}-{author}-{caption}"
