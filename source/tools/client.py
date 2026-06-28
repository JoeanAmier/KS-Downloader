from curl_cffi.requests import AsyncSession

from source.variable import PC_IMPERSONATE, TIMEOUT


def base_client(
    impersonate=PC_IMPERSONATE,
    timeout=TIMEOUT,
    proxy=None,
    **kwargs,
) -> AsyncSession:
    return AsyncSession(
        timeout=timeout,
        verify=False,
        max_clients=10,
        allow_redirects=True,
        impersonate=impersonate,
        proxy=proxy,
        **kwargs,
    )
