from ..translation import _


def retry_request(function):
    async def inner(self, *args, **kwargs):
        if r := await function(self, *args, **kwargs):
            return r
        for i in range(1, self.retry + 1):
            self.console.print(_("正在进行第 {count} 次重试").format(count=i))
            if r := await function(self, *args, **kwargs):
                return r
        return r

    return inner
