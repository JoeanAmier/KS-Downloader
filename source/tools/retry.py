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


def retry_limited(function):
    def inner(self, *args, **kwargs):
        while True:
            if function(self, *args, **kwargs):
                return
            if self.console.input(
                _(
                    "如需重新尝试处理该对象，请关闭所有正在访问该对象的窗口或程序，然后直接按下回车键！\n"
                    "如需跳过处理该对象，请输入任意字符后按下回车键！"
                ),
            ):
                return

    return inner
