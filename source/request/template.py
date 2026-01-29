from json import dumps
from typing import TYPE_CHECKING

from ..tools import capture_error_request, retry_request, wait
from ..translation import _

if TYPE_CHECKING:
    from ..manager import Manager


class APILive:
    DOMAIN: str = "https://live.kuaishou.com"

    def __init__(
        self,
        manager: "Manager",
        cookie: str = "",
        proxy: str = "",
        *args,
        **kwargs,
    ):
        self.client = manager.client
        self.headers = manager.pc_data_headers.copy()
        self.console = manager.console
        self.retry = manager.max_retry
        self.proxy = proxy
        self.note: str = ""
        self.extract_keys: tuple[str, ...] = ()
        self.finished = False
        self.items: list[dict] = []
        self.result = {"data": self.items}
        self.cursor: str = ""
        self.max_batch = 9999
        self.api: str = ""
        self.__set_cookie(cookie)

    def __set_cookie(self, cookie: str):
        pass

    async def run(
        self,
    ):
        # self.set_referer()
        await self.run_batch()
        return self.result | {"cursor": self.cursor}

    # def set_referer(self, referer: str = None) -> None:
    #     self.headers["Referer"] = referer or self.DOMAIN

    async def run_single(
        self,
        *args,
        **kwargs,
    ) -> None:
        await self.get_data(
            self.api,
            params=self.generate_params(),
            data=self.generate_data(),
            method="POST",
        )

    async def run_batch(
        self,
        *args,
        **kwargs,
    ) -> None:
        while not self.finished and self.max_batch > 0:
            await self.run_single(*args, **kwargs)
            self.max_batch -= 1

    async def get_data(
        self,
        url,
        headers=None,
        params=None,
        data=None,
        json=None,
        method="GET",
    ):
        match method:
            case "GET":
                response = await self.__get_data(
                    url,
                    params,
                    headers,
                )
                self.deal_response(
                    response,
                )
            case "POST":
                response = await self.__post_data(
                    url,
                    params,
                    headers,
                    data,
                    json,
                )
                self.deal_response(
                    response,
                )
            case _:
                raise ValueError(f"Invalid method: {method}")

    @retry_request
    @capture_error_request
    async def __post_data(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        data: dict = None,
        json: dict = None,
        **kwargs,
    ) -> dict:
        response = await self.client.post(
            url,
            headers=headers or self.headers,
            params=params,
            data=dumps(data, separators=(",", ":")),
            json=json,
            **kwargs,
        )
        await wait()
        response.raise_for_status()
        return response.json()

    @retry_request
    @capture_error_request
    async def __get_data(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        **kwargs,
    ) -> dict:
        response = await self.client.get(
            url,
            headers=headers or self.headers,
            params=params,
            **kwargs,
        )
        await wait()
        response.raise_for_status()
        return response.json()

    def generate_params(
        self,
        *args,
        **kwargs,
    ) -> dict:
        pass

    def generate_data(
        self,
        *args,
        **kwargs,
    ) -> dict:
        pass

    def deal_response(
        self,
        response: dict | None,
    ) -> None:
        if cursor := response.get("pcursor"):
            self.cursor = cursor
            self.deal_items_response(
                response,
            )
        else:
            self.finished = True
            msg = _("{note}数据响应内容异常：{response}").format(
                note=self.note, response=response
            )
            self.console.error(msg)
            self.result["message"] = msg

    def deal_items_response(
        self,
        response: dict | None,
    ) -> None:
        try:
            for key in self.extract_keys:
                response = response[key]
            if not response:
                msg = _("{note}数据响应内容为空").format(note=self.note)
                self.console.warning(msg)
                self.result["message"] = msg
            else:
                self.add_item(
                    response,
                )
        except (
            KeyError,
            IndexError,
        ):
            msg = _("{note}数据响应内容异常：{response}").format(
                note=self.note, response=response
            )
            self.console.error(msg)
            self.result["message"] = msg

    def add_item(
        self,
        items: list[dict],
        start: int = None,
        end: int = None,
    ) -> None:
        self.items.extend(items[start:end])


class API(APILive):
    DOMAIN: str = "https://www.kuaishou.com"

    def __init__(
        self,
        manager: "Manager",
        cookie: str = "",
        proxy: str = "",
        *args,
        **kwargs,
    ):
        super().__init__(
            manager,
            cookie,
            proxy,
            *args,
            **kwargs,
        )
