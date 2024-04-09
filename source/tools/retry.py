def retry_request(function):
    async def inner(self, *args, **kwargs):
        if r := await function(self, *args, **kwargs):
            return r
        for i in range(1, self.retry + 1):
            self.console.print(f"正在进行第 {i} 次重试")
            if r := await function(self, *args, **kwargs):
                return r
        return r

    return inner
