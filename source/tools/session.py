from aiohttp import ClientSession
from aiohttp import ClientTimeout

from source.variable import PC_USERAGENT
from source.variable import TIMEOUT


def base_session(
        user_agent=PC_USERAGENT,
        timeout=TIMEOUT,
) -> ClientSession:
    return ClientSession(
        headers={"User-Agent": user_agent, },
        timeout=ClientTimeout(connect=timeout),
    )
