def cookie_str_to_dict(cookie_str: str) -> dict:
    """将 cookie 字符串转为字典格式

    Args:
        cookie_str: cookie 字符串，格式为 "key1=value1; key2=value2"

    Returns:
        字典格式的 cookie
    """
    if not cookie_str:
        return {}

    cookie_dict = {}
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            key, value = item.split("=", 1)
            cookie_dict[key.strip()] = value.strip()
    return cookie_dict


def cookie_dict_to_str(cookie_dict: dict) -> str:
    """将字典格式的 cookie 转为字符串

    Args:
        cookie_dict: 字典格式的 cookie

    Returns:
        cookie 字符串，格式为 "key1=value1; key2=value2"
    """
    if not cookie_dict:
        return ""

    return "; ".join(f"{key}={value}" for key, value in cookie_dict.items())
