from asyncio import sleep
from random import lognormvariate
from math import log


def get_wait_time(
    avg_delay: float | int = 6.0,
    sigma: float = 0.6,
) -> float:
    mu = log(avg_delay) - (sigma**2 / 2)
    delay = lognormvariate(mu, sigma)
    min_delay = avg_delay * 0.2
    max_delay = avg_delay * 4.0
    return max(min_delay, min(max_delay, delay))


async def wait(
    avg_delay: float | int = 6.0,
) -> None:
    await sleep(get_wait_time(avg_delay=avg_delay))
