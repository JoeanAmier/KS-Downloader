PC_USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
    "Safari/537.36")
APP_USERAGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/16.6 Mobile/15E148 Safari/604.1")
SEC_CH_UA = '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"'
Cookie = '"kpf=PC_WEB; clientid=3; did=web_eda1a93f1f2a99778b3dea2ed60fc496; arp_scroll_position=0; userId=3568785353; kpn=KUAISHOU_VISION; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABudUVe1aunIWZSj6PE3uzs67cNzH-u5iyM44cD-NrZMfYX3CxZhlerbs70kawwFNxwO_THqC0Nf4gJX8NLg72iiXDKhf2WyPRNrL-JplI6wpbEMT_hQld8muKZD679iFrkGtXHiCA4391rkmAE2COAE8E2wf6_mY43fH7Ccbbaqks3K1hBdx62P-xvWbRjj0714LEf09TPgN-W8BkJeNdgxoStEyT9S95saEmiR8Dg-bb1DKRIiBsiinsiplsExnD2Hh-ZL1z_pdtWpKi_aIQWjmGfN17MigFMAE; kuaishou.server.web_ph=ad0f7ffe552ff2aa87ae7270235d15d81d32"'
PC_PAGE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': PC_USERAGENT,
    'sec-ch-ua': SEC_CH_UA,
    "Cookie": Cookie,
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
PC_DATA_HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    "Cookie": Cookie,
    'User-Agent': PC_USERAGENT,
    'Accept': '*/*',
    'sec-ch-ua': SEC_CH_UA,
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
APP_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Host": "v.kuaishou.com",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Cookie": Cookie,
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": APP_USERAGENT,
}
APP_DATA_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en,ja;q=0.9,zh-CN;q=0.8,zh-HK;q=0.7,zh;q=0.6",
    "Content-Type": "application/json",
    # "Origin": "https://v.m.chenzhongtech.com",
    "Host": "m.gifshow.com",
    "Origin": "https://m.gifshow.com",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Referer": "",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Cookie": Cookie,
    # "Sec-Fetch-User": "?1",
    "User-Agent": APP_USERAGENT,
}
APP_DOWNLOAD_HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "Cookie": Cookie,
    "Upgrade-Insecure-Requests": '1',
    "user-agent": APP_USERAGENT,
}
TIMEOUT = 10
RETRY = 2
