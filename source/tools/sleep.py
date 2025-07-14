from asyncio import sleep
from random import uniform


async def wait(min_delay: float | int = 1, max_delay: float | int = 2) -> None:
    """Sleep for a random amount of time between min_delay and max_delay seconds.

    Args:
        min_delay: Minimum delay in seconds. Defaults to 1.
        max_delay: Maximum delay in seconds. Defaults to 2.5.
    """
    await sleep(uniform(min_delay, max_delay))
