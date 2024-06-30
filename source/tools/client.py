from httpx import AsyncClient
from httpx import Limits

from source.variable import PC_USERAGENT
from source.variable import TIMEOUT


def base_client(
        user_agent=PC_USERAGENT,
        timeout=TIMEOUT,
        **kwargs,
) -> AsyncClient:
    return AsyncClient(
        headers={"User-Agent": user_agent, },
        timeout=timeout,
        verify=False,
        limits=Limits(max_connections=10),
        follow_redirects=True,
        **kwargs,
    )
