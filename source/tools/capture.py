from json.decoder import JSONDecodeError

from httpx import HTTPError


def capture_error_request(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except HTTPError as e:
            self.console.error(f"网络异常：{e}")
        except JSONDecodeError as e:
            self.console.error(f"响应内容异常：{e}")
        return None

    return inner
