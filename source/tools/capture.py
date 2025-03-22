from json.decoder import JSONDecodeError

from httpx import HTTPError

from ..module import CacheError
from ..translation import _


def capture_error_request(function):
    async def inner(self, *args, **kwargs):
        try:
            return await function(self, *args, **kwargs)
        except HTTPError as e:
            self.console.error(_("网络异常：{error}").format(error=repr(e)))
        except JSONDecodeError as e:
            self.console.error(_("响应内容异常：{error}").format(error=repr(e)))
        except PermissionError as e:
            self.console.error(_("权限异常：{error}").format(error=repr(e)))
        except CacheError as e:
            self.console.error(e)
        return None

    return inner
