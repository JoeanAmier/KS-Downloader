from json import dumps
from typing import TYPE_CHECKING
from ..variable import PC_DATA_HEADERS
from curl_cffi.requests import post, get
from ..tools import capture_error_request, retry_request, wait
from ..translation import _

if TYPE_CHECKING:
    from ..manager import Manager


class APILive:
    DOMAIN: str = "https://live.kuaishou.com"

    def __init__(
        self,
        manager: "Manager",
        cookies: str | dict = "",
        proxy: str = "",
        *args,
        **kwargs,
    ):
        self.client = manager.client  # client_api
        self.timeout = manager.timeout
        self.cookies = cookies
        self.impersonate = manager.impersonate
        self.console = manager.console
        self.max_retry = manager.max_retry
        self.proxy = proxy
        self.note: str = ""
        self.extract_keys: tuple[str, ...] = ()
        self.finished = False
        self.items: list[dict] = []
        self.result = {"data": self.items}
        self.cursor: str = ""
        self.max_batch = 9999
        self.api: str = ""

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
        params=None,
        data=None,
        json=None,
        method="GET",
    ):
        match (method, any((self.cookies, self.proxy))):
            case ("GET", False):
                response = await self.__get_data(
                    url,
                    params,
                )
                self.deal_response(
                    response,
                )
            case ("POST", False):
                response = await self.__post_data(
                    url,
                    params,
                    data,
                    json,
                )
                self.deal_response(
                    response,
                )
            case ("POST", True):
                response = await self.__post_data_disposable(
                    url,
                    params,
                    data,
                    json,
                )
                self.deal_response(
                    response,
                )
            case ("GET", True):
                response = await self.__get_data_disposable(
                    url,
                    params,
                )
                self.deal_response(
                    response,
                )
            case __:
                raise ValueError(f"Invalid method: {method}")

    @retry_request
    @capture_error_request
    async def __post_data(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        **kwargs,
    ) -> dict:
        response = await self.client.post(
            url,
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
    async def __post_data_disposable(
        self,
        url: str,
        params: dict | None = None,
        data: dict | None = None,
        json: dict | None = None,
        **kwargs,
    ) -> dict:
        response = post(
            url,
            params=params,
            data=dumps(data, separators=(",", ":")),
            json=json,
            timeout=self.timeout,
            headers=PC_DATA_HEADERS | {"Cookie": self.cookies},
            verify=False,
            proxy=self.proxy,
            impersonate=self.impersonate,
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
        params: dict | None = None,
        **kwargs,
    ) -> dict:
        response = await self.client.get(
            url,
            params=params,
            **kwargs,
        )
        await wait()
        response.raise_for_status()
        return response.json()

    @retry_request
    @capture_error_request
    async def __get_data_disposable(
        self,
        url: str,
        params: dict | None = None,
        **kwargs,
    ) -> dict:
        response = get(
            url,
            params=params,
            timeout=self.timeout,
            headers=PC_DATA_HEADERS | {"Cookie": self.cookies},
            verify=False,
            proxy=self.proxy,
            impersonate=self.impersonate,
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
        if cursor := response.get("pcursor", ""):
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
        start: int | None = None,
        end: int | None = None,
    ) -> None:
        self.items.extend(items[start:end])


class API(APILive):
    DOMAIN: str = "https://www.kuaishou.com"

    def __init__(
        self,
        manager: "Manager",
        cookies: str = "",
        proxy: str = "",
        *args,
        **kwargs,
    ):
        super().__init__(
            manager,
            cookies,
            proxy,
            *args,
            **kwargs,
        )
