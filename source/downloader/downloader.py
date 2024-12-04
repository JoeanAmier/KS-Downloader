from asyncio import Semaphore
from asyncio import gather
from pathlib import Path
from shutil import move
from typing import TYPE_CHECKING

from aiofiles import open
from httpx import HTTPError
from rich.progress import (
    SpinnerColumn,
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)

from ..module import CacheError
from ..tools import (
    PROGRESS,
)
from ..tools import beautify_string
from ..tools import capture_error_request
from ..tools import retry_request

if TYPE_CHECKING:
    from ..manager import Manager
    from ..module import Database


class Downloader:
    CONTENT_TYPE_MAP = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
        "video/mp4": "mp4",
        "video/quicktime": "mov",
        "audio/mp4": "m4a",
        "audio/mpeg": "mp3",
    }

    def __init__(self, manager: "Manager", database: "Database"):
        self.path = manager.path
        self.folder = manager.folder
        self.client = manager.client
        self.headers = manager.pc_download_headers
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
        self.name_format = manager.name_format

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

    async def run(self, data: list[dict], type_="detail", ):
        match type_:
            case "detail":
                await self.__handle_detail(data, )
            case "user":
                pass
            case _:
                raise ValueError

    async def __handle_detail(self, data: list[dict], ):
        tasks = []
        with self.__general_progress_object() as progress:
            for item in data:
                if await self.database.has_download_data(i := item["detailID"]):
                    self.console.info(f"作品 {i} 存在下载记录，跳过下载！")
                    continue
                name = self.__generate_name(item, )
                match item["photoType"]:
                    case "视频":
                        await self.__handle_video(tasks, name, item, progress, )
                    case "图片":
                        await self.__handle_atlas(tasks, name, item, progress, )
                    case _:
                        self.console.error("未知的作品类型")
                # await self.__handle_music(tasks, name, item, progress, )
            await gather(*tasks)

    async def __handle_music(self, tasks: list, name: str, data: dict, progress: Progress, ):
        if not self.music or not (m := data.get("audioUrls")):
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
                data["download"][0],
                file,
                progress,
                data["detailID"],
                "视频",
            ))
        # await self.__handle_cover(tasks, file, data, progress, )

    async def __handle_atlas(self, tasks: list, name: str, data: dict, progress: Progress, ):
        urls = data["download"]
        for index, url in enumerate(urls, start=1):
            file = self.__generate_path(f"{name}_{index}")
            if not self.__file_exists(file, "webp", ):
                tasks.append(self.__download_file(
                    url,
                    file,
                    progress,
                    data["detailID"],
                    "图片",
                ))

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
            text = beautify_string(path.name, 50)
            if not url:
                self.console.warning(f"【{tip}】{text} 下载链接为空")
                return True
            headers = self.headers.copy()
            length, suffix = await self.__head_file(url, headers, )
            temp = self.temp.joinpath(f"{path.name}.{suffix}")
            path = path.with_name(f"{path.name}.{suffix}")
            position = self.__update_headers_range(headers, temp, length, )
            try:
                # print("stream", headers.get("Range"))  # 调试代码
                async with self.client.stream("GET", url, headers=headers, ) as response:
                    if response.status_code == 416:
                        self.delete(temp)
                        raise CacheError(f"【{tip}】{text} 缓存异常，重新下载")
                    response.raise_for_status()
                    task_id = progress.add_task(
                        f"【{tip}】{text}",
                        total=length or None,
                        completed=position,
                    )
                    async with open(temp, "ab") as f:
                        async for chunk in response.aiter_bytes(self.chunk):
                            await f.write(chunk)
                            progress.update(task_id, advance=len(chunk))
            except HTTPError as e:
                await self.database.delete_download_data(id_)
                raise HTTPError(repr(e)) from e
            self.move(temp, path)
            self.console.info(f"【{tip}】{text} 下载完成")
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
    def delete(temp: "Path", ):
        if temp.is_file():
            temp.unlink()

    @staticmethod
    def move(temp: "Path", path: "Path"):
        move(temp.resolve(), path.resolve())

    def __file_exists(self, path: "Path", suffix="*") -> bool:
        if e := any(path.parent.glob(n := f"{path.name}.{suffix}")):
            self.console.info(f"{n} 已存在，跳过下载")
        return e

    def __generate_name(self, data: dict, app: bool = False, ) -> str:
        name = []
        for i in self.name_format:
            match i:
                case "作品类型":
                    name.append(self.__get_type(data))
                case "发布日期":
                    name.append(self.__get_date(data))
                case "作者昵称":
                    name.append(self.__get_author_nickname(data, app, ))
                case "作者ID":
                    name.append(self.__get_author_id(data, app, ))
                case "作品描述":
                    name.append(self.__get_caption(data)
                                or self.__get_detail_id(data))
                case "作品ID":
                    name.append(self.__get_detail_id(data))
        return beautify_string("_".join(name), length=128, )

    @staticmethod
    def __get_type(data: dict, ):
        return data["photoType"]

    @staticmethod
    def __get_date(data: dict, ):
        return data["timestamp"].replace(":", ".")

    def __get_author_nickname(self, data: dict, app: bool, ) -> str:
        return (
            self.cleaner.filter_name(data["userName"]) or data["userEid"]
            if app
            else self.cleaner.filter_name(data["name"]) or data["authorId"]
        )

    @staticmethod
    def __get_author_id(data: dict, app: bool, ) -> str:
        return data["userEid"] if app else data["authorId"]

    def __get_caption(self, data: dict, ):
        return self.cleaner.filter_name(
            self.cleaner.clear_spaces(
                data["caption"]))

    @staticmethod
    def __get_detail_id(data: dict, ):
        return data["detailID"]

    def __generate_root(self, name: str, ) -> Path:
        return self.folder.joinpath(name) if self.folder_mode else self.folder

    def __generate_path(self, name: str, ) -> Path:
        root = self.__generate_root(name)
        root.mkdir(exist_ok=True)
        return root.joinpath(name)

    async def __head_file(
            self,
            url: str,
            headers: dict,
    ) -> [int, str]:
        # print("head", headers.get("Range"))  # 调试代码
        response = await self.client.head(
            url,
            headers=headers,
        )
        response.raise_for_status()
        suffix = self.__extract_type(
            response.headers.get("Content-Type"))
        length = response.headers.get(
            "Content-Length", 0)
        return int(length), suffix

    @staticmethod
    def __get_resume_byte_position(file: Path) -> int:
        return file.stat().st_size if file.is_file() else 0

    def __update_headers_range(
            self, headers: dict, file: Path, length: int, ) -> int:
        position = self.__get_resume_byte_position(file)
        if length and position >= length:
            self.delete(file)
            position = 0
        headers["Range"] = f"bytes={position}-"
        return position
