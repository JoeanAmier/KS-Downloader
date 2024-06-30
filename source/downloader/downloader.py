from asyncio import Semaphore
from asyncio import gather
from pathlib import Path
from shutil import move
from typing import TYPE_CHECKING

from httpx import HTTPError
from rich.progress import (
    SpinnerColumn,
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from source.tools import (
    PROGRESS,
)
from source.tools import capture_error_request
from source.tools import retry_request
from source.tools import truncation

if TYPE_CHECKING:
    from source.manager import Manager
    from source.module import Database


class Downloader:
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
        "audio/mp4": "m4a"
    }

    def __init__(self, manager: "Manager", database: "Database"):
        self.path = manager.path
        self.folder = manager.folder
        self.client = manager.client
        self.headers = manager.app_download_headers
        self.cleaner = manager.cleaner
        self.cover = manager.cover
        self.music = manager.music
        self.console = manager.console
        self.retry = manager.max_retry
        self.temp = manager.temp
        self.folder_mode = manager.folder_mode
        self.chunk = manager.chunk
        self.semaphore = Semaphore(manager.max_workers)
        self.database = database

    def __general_progress_object(self) -> Progress:
        return Progress(
            TextColumn(
                "[progress.description]{task.description}",
                style=PROGRESS,
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

    async def run(self, data: list[dict], type_="detail", app=True, ):
        match type_:
            case "detail":
                await self.__handle_detail(data, app, )
            case "user":
                pass
            case _:
                raise ValueError

    async def __handle_detail(self, data: list[dict], app: bool, ):
        tasks = []
        with self.__general_progress_object() as progress:
            for item in data:
                if await self.database.has_download_data(i := item["detailID"]):
                    self.console.info(f"作品 {i} 存在下载记录，跳过下载！")
                    continue
                name = self.__generate_name(item, app, )
                match item["photoType"]:
                    case "视频":
                        await self.__handle_video(tasks, name, item, progress, )
                    case "图片":
                        await self.__handle_atlas(tasks, name, item, progress, )
                    case _:
                        self.console.error("未知的作品类型")
                await self.__handle_music(tasks, name, item, progress, )
            await gather(*tasks)

    async def __handle_music(self, tasks: list, name: str, data: dict, progress: Progress, ):
        if not (m := data.get("audioUrls")):
            return
        file = self.__generate_path(name)
        if not self.__file_exists(file, "m4a"):
            tasks.append(self.__download_file(
                m.split()[0],
                file,
                progress,
                data["detailID"],
                "音乐",
            ))

    async def __handle_video(self, tasks: list, name: str, data: dict, progress: Progress, ):
        file = self.__generate_path(name)
        if not self.__file_exists(file, "mp4"):
            tasks.append(self.__download_file(
                data["download"], file, progress, data["detailID"], "视频", ))
        await self.__handle_cover(tasks, file, data, progress, )

    async def __handle_atlas(self, tasks: list, name: str, data: dict, progress: Progress, ):
        urls = data["download"].split()
        for index, url in enumerate(urls, start=1):
            file = self.__generate_path(f"{name}_{index}")
            if not self.__file_exists(file, ):
                tasks.append(self.__download_file(
                    url, file, progress, data["detailID"], "图片", ))

    async def __handle_cover(self, tasks: list, path: "Path", data: dict, progress: Progress, ):
        match self.cover:
            case "WEBP":
                if not self.__file_exists(path, "webp"):
                    tasks.append(
                        self.__download_file(
                            data.get("webpCoverUrls"),
                            path,
                            progress,
                            data["detailID"],
                            "封面",
                        ))
            case "JPEG":
                if not self.__file_exists(path, "jpeg"):
                    tasks.append(
                        self.__download_file(
                            data.get("coverUrls"),
                            path,
                            progress,
                            data["detailID"],
                            "封面",
                        ))
            case "":
                pass

    @retry_request
    @capture_error_request
    async def __download_file(self, url: str, path: "Path", progress: Progress, id_: str, tip: str = ""):
        async with self.semaphore:
            if not url:
                self.console.warning(f"【{tip}】{truncation(path.name)} 下载链接为空")
                return True
            try:
                async with self.client.stream("GET", url, headers=self.headers, ) as response:
                    response.raise_for_status()
                    suffix = self.__extract_type(
                        response.headers.get("Content-Type"))
                    temp = self.temp.joinpath(f"{path.name}.{suffix}")
                    path = path.with_name(f"{path.name}.{suffix}")
                    task_id = progress.add_task(
                        f"【{tip}】{truncation(path.name)}", total=int(
                            response.headers.get(
                                "Content-Length", "0")) or None)
                    with temp.open("wb") as f:
                        async for chunk in response.aiter_bytes(self.chunk):
                            f.write(chunk)
                            progress.update(task_id, advance=len(chunk))
            except HTTPError as e:
                self.console.error(
                    f"【{tip}】{truncation(path.name)} 网络异常: {e}")
                await self.database.delete_download_data(id_)
                return False
            self.move(temp, path)
            self.console.info(f"【{tip}】{truncation(path.name)} 下载完成")
            await self.database.write_download_data(id_)
            return True

    def __extract_type(self, content: str) -> str:
        if not (s := self.CONTENT_TYPE_MAP.get(content)):
            return self.__unknown_type(content)
        return s

    def __unknown_type(self, content: str) -> str:
        self.console.error(f"未知的文件类型：{content}")
        return ""

    @staticmethod
    def move(temp: "Path", path: "Path"):
        move(temp.resolve(), path.resolve())

    def __file_exists(self, path: "Path", suffix="*") -> bool:
        if e := any(path.parent.glob(n := f"{path.name}.{suffix}")):
            self.console.info(f"{n} 已存在，跳过下载")
        return e

    def __generate_name(self, data: dict, app: bool, ) -> str:
        type_ = data["photoType"]
        date = data["timestamp"].replace(":", ".")
        author = self.__generate_author_info(data, app, )
        caption = self.cleaner.filter_name(
            self.cleaner.clear_spaces(
                data["caption"])) or data["detailID"]
        return f"{type_}-{date}-{author}-{caption}"

    def __generate_author_info(self, data: dict, app: bool, ) -> str:
        return (
            self.cleaner.filter_name(data["userName"]) or data["userEid"]
            if app
            else self.cleaner.filter_name(data["name"]) or data["authorId"]
        )

    def __generate_root(self, name: str, ) -> Path:
        return self.folder.joinpath(name) if self.folder_mode else self.folder

    def __generate_path(self, name: str, ) -> Path:
        root = self.__generate_root(name)
        root.mkdir(exist_ok=True)
        return root.joinpath(name)
