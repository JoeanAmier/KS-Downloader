PC_USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
    "Safari/537.36")
APP_USERAGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/16.6 Mobile/15E148 Safari/604.1")
SEC_CH_UA = '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
PC_PAGE_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Sec-Fetch-Dest': 'document',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Site': 'none',
    # 'Sec-Fetch-User': '?1',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': PC_USERAGENT,
    # 'Sec-Ch-Ua': SEC_CH_UA,
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
}
PC_DATA_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    'User-Agent': PC_USERAGENT,
    # 'Sec-Ch-Ua': SEC_CH_UA,
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
}
APP_HEADERS = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "*/*",
    "Host": "v.kuaishou.com",
    # "Sec-Fetch-Dest": "document",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-Site": "none",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": APP_USERAGENT,
}
APP_DATA_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "*/*",
    "Accept-Language": "en,ja;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh;q=0.6",
    "Content-Type": "application/json",
    # "Origin": "https://v.m.chenzhongtech.com",
    "Host": "m.gifshow.com",
    "Origin": "https://m.gifshow.com",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Referer": "",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    # "Sec-Fetch-User": "?1",
    "User-Agent": APP_USERAGENT,
}
APP_DOWNLOAD_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "*/*",
    # "Upgrade-Insecure-Requests": '1',
    "User-Agent": APP_USERAGENT,
}
TIMEOUT = 10
RETRY = 5
