from typing import TYPE_CHECKING

from ..tools import capture_error_request, retry_request, wait
from ..translation import _

if TYPE_CHECKING:
    from ..manager import Manager


class API:
    DOMAIN: str = "https://live.kuaishou.com"

    def __init__(
        self,
        manager: "Manager",
        *args,
        **kwargs,
    ):
        self.client = manager.client
        self.headers = manager.pc_data_headers
        self.console = manager.console
        self.retry = manager.max_retry
        self.note: str = ""
        self.extract_keys: tuple[str, ...] = ()
        self.finished = False
        self.items: list[dict] = []
        self.api: str = ""

    async def run(
        self,
        *args,
        **kwargs,
    ):
        return self.items

    async def run_single(
        self,
        *args,
        **kwargs,
    ):
        pass

    async def run_batch(
        self,
        *args,
        **kwargs,
    ):
        pass

    async def get_data(
        self,
        url,
        headers=None,
        params=None,
        data=None,
        json=None,
        method="GET",
        *args,
        **kwargs,
    ):
        match method:
            case "GET":
                response = await self.__get_data(
                    url,
                    params,
                    headers,
                    *args,
                    **kwargs,
                )
            case "POST":
                response = await self.__post_data(
                    url,
                    params,
                    headers,
                    data,
                    json,
                    *args,
                    **kwargs,
                )
            case _:
                raise ValueError(f"Invalid method: {method}")
        self.deal_response(
            response,
        )

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
    ):
        response = await self.client.post(
            url,
            headers=headers or self.headers,
            params=params,
            data=data,
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
    ):
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
        *args,
        **kwargs,
    ) -> None:
        try:
            for key in self.extract_keys:
                response = response[key]
            self.add_item(
                response,
            )
        except (
            KeyError,
            IndexError,
        ):
            self.console.error(
                _("{note}数据响应内容异常：{response}").format(
                    note=self.note, response=response
                )
            )

    def add_item(
        self,
        items: list[dict],
        start: int = None,
        end: int = None,
    ) -> None:
        if items:
            self.items.extend(items[start:end])
        else:
            self.console.warning(_("{note}数据响应内容为空").format(note=self.note))
