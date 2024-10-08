from re import compile
from typing import TYPE_CHECKING
from urllib.parse import urlparse, parse_qs

from source.tools import capture_error_request
from source.tools import retry_request

if TYPE_CHECKING:
    from source.manager import Manager


class Detail:
    # API = "https://v.m.chenzhongtech.com/rest/wd/photo/info?kpn=KUAISHOU"
    API = "https://m.gifshow.com/rest/wd/photo/info?kpn=undefined&captchaToken=&__NS_sig3="
    ID = compile(r"short-video/([^\s?]+)")

    def __init__(self, manager: "Manager"):
        self.client = manager.client
        self.headers = manager.app_data_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.params = {
            # "fid": None,
            # "shareToken": None,
            # "shareObjectId": None,
            # "shareMethod": "TOKEN",
            # "shareId": None,
            # "shareResourceType": "PHOTO_OTHER",
            # "shareChannel": "share_copylink",
            # "kpn": "KUAISHOU",
            # "subBiz": "BROWSE_SLIDE_PHOTO",
            "env": "SHARE_VIEWER_ENV_TX_TRICK",
            # "h5Domain": "v.m.chenzhongtech.com",
            "h5Domain": "m.gifshow.com",
            "photoId": "",
            "isLongVideo": False,
        }

    async def run(self, url: str, ):
        link = urlparse(url)
        params = parse_qs(link.query)
        if not (id_ := params.get("photoId", self.__extract_id(url))[0]):
            self.console.warning("提取作品 ID 失败")
            return None
        self.headers["Referer"] = url
        self.__update_params(params, id_)
        if not (d := await self.__get_data()):
            self.console.warning("请求作品数据失败，接口可能已经失效！")
            return None
        if e := d.get("error_msg"):
            self.console.warning(f"请求作品数据错误：{e}")
            return None
        return d

    @retry_request
    @capture_error_request
    async def __get_data(self):
        response = await self.client.post(self.API, headers=self.headers, json=self.params, )
        response.raise_for_status()
        return response.json()

    def __extract_id(self, url: str) -> list:
        return [i.group(1)] if (i := self.ID.search(url)) else [None]

    def __update_params(self, params: dict, id_: str):
        # self.params["fid"] = self.__extract_key(params, "fid")
        # self.params["shareToken"] = self.__extract_key(params, "shareToken")
        # self.params["shareObjectId"] = self.__extract_key(
        #     params, "shareObjectId")
        # self.params["shareId"] = self.__extract_key(params, "shareId")
        self.params["photoId"] = id_

    @staticmethod
    def __extract_key(data: dict, key: str):
        return data.get(key, [""])[0]
