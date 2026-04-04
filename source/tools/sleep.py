from asyncio import sleep
from random import lognormvariate
from math import log


def get_wait_time(
    avg_delay: float | int = 6.0,
    sigma: float = 0.6,
) -> float:
    mu = log(avg_delay) - (sigma**2 / 2)
    return max(0.5, lognormvariate(mu, sigma))


async def wait() -> None:
    await sleep(get_wait_time())
