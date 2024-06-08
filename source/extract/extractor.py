from datetime import datetime
from time import localtime
from time import strftime
from types import SimpleNamespace
from typing import TYPE_CHECKING
from urllib.parse import parse_qs

from lxml.etree import HTML
from yaml import safe_load

from source.tools import Namespace

if TYPE_CHECKING:
    from source.manager import Manager


class PageExtractor:
    APOLLO_STATE = "//script/text()"

    def __init__(self, manager: "Manager"):
        self.date_format = "%Y-%m-%d_%H:%M:%S"
        self.console = manager.console
        self.cleaner = manager.cleaner

    def run(self, html: str, id_: str, ) -> dict:
        if not (data := self.__convert_object(self.__extract_object(html))):
            self.console.warning("提取数据失败")
            return {}
        data = Namespace(data)
        return self.__extract_detail(data, id_)

    def __extract_object(self, html: str) -> str:
        if not html:
            return ""
        html_tree = HTML(html)
        return d[1] if (d := html_tree.xpath(self.APOLLO_STATE)) else ""

    @staticmethod
    def __convert_object(text: str) -> dict:
        text = text.lstrip("window.__APOLLO_STATE__=")
        text = text.replace(
            ";(function(){var s;(s=document.currentScript||document.scripts["
            "document.scripts.length-1]).parentNode.removeChild(s);}());", "")
        return safe_load(text)

    def __extract_detail(self, data: Namespace, id_: str) -> dict:
        container = {
            "collection_time": datetime.now().strftime(
                self.date_format),
            "photoType": "视频",
        }
        data = data.safe_extract("defaultClient")
        detail = f"VisionVideoDetailPhoto:{id_}"
        if not Namespace.object_extract(data, detail):
            return {}
        container["detailID"] = id_
        container["caption"] = Namespace.object_extract(
            data, f"{detail}.caption")
        container["coverUrl"] = Namespace.object_extract(
            data, f"{detail}.coverUrl")
        container["duration"] = APIExtractor.time_conversion(
            Namespace.object_extract(data, f"{detail}.duration", 0))
        container["realLikeCount"] = Namespace.object_extract(
            data, f"{detail}.realLikeCount")
        container["download"] = Namespace.object_extract(
            data, f"{detail}.photoUrl")
        container["timestamp"] = APIExtractor.format_date(
            Namespace.object_extract(
                data, f"{detail}.timestamp", 0), self.date_format, )
        container["viewCount"] = Namespace.object_extract(
            data, f"{detail}.viewCount")
        self.__extract_author(container, data)
        return container

    @staticmethod
    def __extract_author(container: dict, data: Namespace) -> None:
        author = next(
            (
                getattr(data, i)
                for i in dir(data)
                if "VisionVideoDetailAuthor:" in i
            ),
            None,
        )
        container["authorID"] = Namespace.object_extract(author, "id")
        container["name"] = Namespace.object_extract(author, "name")


class APIExtractor:
    PHOTO_TYPE = {
        "VIDEO": "视频",
        "VERTICAL_ATLAS": "图片",
        "HORIZONTAL_ATLAS": "图片",
    }
    USER_SEX = {
        "F": "女",
        "": "未知",
        "M": "男",
    }

    def __init__(self, manager: "Manager"):
        self.date_format = "%Y-%m-%d_%H:%M:%S"
        self.console = manager.console
        self.cleaner = manager.cleaner

    @staticmethod
    def generate_data_object(
            data: dict) -> SimpleNamespace | list[SimpleNamespace]:
        return Namespace.generate_data_object(data)

    @staticmethod
    def safe_extract(
            data: SimpleNamespace,
            attribute_chain: str,
            default: str | int | list | dict | SimpleNamespace = ""):
        attributes = attribute_chain.split(".")
        for attribute in attributes:
            if "[" in attribute:
                parts = attribute.split("[", 1)
                attribute = parts[0]
                index = parts[1].split("]", 1)[0]
                try:
                    index = int(index)
                    data = getattr(data, attribute, None)[index]
                except (IndexError, TypeError, ValueError):
                    return default
            else:
                data = getattr(data, attribute, None)
                if not data:
                    return default
        return data or default

    def run(self, data: list[dict], type_="detail") -> list[dict]:
        container = []
        if not data:
            return container
        match type_:
            case "detail":
                [self.__extract_items(
                    container, self.generate_data_object(item)) for item in data]
            case "user":
                pass
            case _:
                raise ValueError
        return container

    def __extract_items(self, container: list, data: SimpleNamespace) -> None:
        item = {
            "collection_time": datetime.now().strftime(
                self.date_format), }
        self.__extract_comments(item, data)
        self.__extract_counts(item, data)
        self.__extract_photo(item, data)
        match item["photoType"]:
            case "视频":
                self.__extract_music(item, data, True)
                self.__extract_mp4(item, data)
            case "图片":
                self.__extract_music(item, data, False)
                self.__extract_atlas(item, data)
            case _:
                item["download"] = ""
        container.append(item)

    def __extract_comments(self, item: dict, data: SimpleNamespace) -> None:
        pass

    def __extract_counts(self, item: dict, data: SimpleNamespace) -> None:
        item["fanCount"] = self.safe_extract(data, "counts.fanCount", -1)
        item["followCount"] = self.safe_extract(data, "counts.followCount", -1)
        item["collectionCount"] = self.safe_extract(
            data, "counts.collectionCount", -1)
        item["photoCount"] = self.safe_extract(data, "counts.photoCount", -1)

    def __extract_photo(self, item: dict, data: SimpleNamespace) -> None:
        photo = self.safe_extract(data, "photo")
        item["timestamp"] = self.format_date(
            self.safe_extract(photo, "timestamp", 0), self.date_format, )
        item["duration"] = self.time_conversion(
            self.safe_extract(photo, "duration", 0))
        item["userName"] = self.safe_extract(photo, "userName")
        item["userId"] = self.safe_extract(photo, "userId")
        item["commentCount"] = self.safe_extract(photo, "commentCount", 0)
        item["viewCount"] = self.safe_extract(photo, "viewCount", 0)
        self.__extract_cover(item, photo)
        item["height"] = self.safe_extract(photo, "height", -1)
        item["width"] = self.safe_extract(photo, "width", -1)
        item["likeCount"] = self.safe_extract(photo, "likeCount", -1)
        item["userSex"] = self.safe_extract(photo, "userSex")
        item["photoType"] = self.PHOTO_TYPE.get(
            self.safe_extract(photo, "photoType"), "未知")
        item["caption"] = self.safe_extract(photo, "caption")
        item["userEid"] = self.safe_extract(photo, "userEid")
        item["detailID"] = self.__extract_id(
            self.safe_extract(photo, "share_info"))

    def __extract_music(self, item: dict, data: SimpleNamespace, video=True, ) -> None:
        if video:
            music = self.safe_extract(data, "photo.soundTrack")
        else:
            music = self.safe_extract(data, "photo.music")
        item["music_name"] = self.safe_extract(music, "name")
        item["audioUrls"] = []
        for i in self.safe_extract(music, "audioUrls", []):
            item["audioUrls"].append(i.url)
        item["audioUrls"] = " ".join(i for i in item["audioUrls"] if i)

    @staticmethod
    def __extract_id(share: str):
        parsed = parse_qs(share)
        return parsed.get("photoId", ["Unknown"])[0]

    def __extract_cover(
            self,
            item: dict,
            photo: SimpleNamespace,
            index=0) -> None:
        cover_urls = self.safe_extract(photo, "coverUrls", )
        item["coverUrls"] = cover_urls[index].url if cover_urls else ""
        webp_cover_urls = self.safe_extract(photo, "webpCoverUrls", )
        item["webpCoverUrls"] = webp_cover_urls[index].url if webp_cover_urls else ""
        head_urls = self.safe_extract(photo, "headUrls", )
        item["headUrls"] = head_urls[index].url if head_urls else ""

    def __extract_mp4(self, item: dict, data: SimpleNamespace) -> None:
        item["download"] = self.safe_extract(data, "mp4Url")

    def __extract_atlas(
            self,
            item: dict,
            data: SimpleNamespace,
            index=0) -> None:
        try:
            cdn = self.safe_extract(data, "atlas.cdn")
            cdn = cdn[index]
        except IndexError:
            cdn = None
        if not cdn:
            item["download"] = ""
            return
        atlas = self.safe_extract(data, "atlas.list")
        urls = [f"https://{cdn}{i}" for i in atlas]
        item["download"] = " ".join(urls)

    @staticmethod
    def format_date(timestamp: int, format_: str, ) -> str:
        if timestamp > 0:
            return strftime(
                format_,
                localtime(timestamp / 1000))
        return "unknown"

    @staticmethod
    def time_conversion(time_: int) -> str:
        if time_ == 0:
            return "00:00:00"
        second = time_ // 1000
        return f"{
        second //
        3600:0>2d}:{
        second %
        3600 //
        60:0>2d}:{
        second %
        3600 %
        60:0>2d}"
