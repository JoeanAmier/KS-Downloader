PC_USERAGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 "
                "Safari/537.36")

APP_USERAGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/16.6 Mobile/15E148 Safari/604.1")

PC_PAGE_HEADERS = {
    "Connection": "keep-alive",
    "Referer": "https://www.kuaishou.cn/new-reco",
    "User-Agent": PC_USERAGENT,
}

PC_DATA_HEADERS = {
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Referer": "https://www.kuaishou.cn",
    "User-Agent": PC_USERAGENT,
}

PC_DOWNLOAD_HEADERS = {
    "User-Agent": PC_USERAGENT,
}

APP_HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": APP_USERAGENT,
}

APP_DATA_HEADERS = {
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Origin": "https://v.m.chenzhongtech.com",
    "Referer": "https://v.m.chenzhongtech.com/",
    "User-Agent": APP_USERAGENT,
}

APP_DOWNLOAD_HEADERS = {
    "User-Agent": APP_USERAGENT,
}

TIMEOUT = 10

RETRY = 5

FILE_SIGNATURES: tuple[tuple[int, bytes, str,], ...] = (
    # 分别为偏移量(字节)、十六进制签名、后缀
    # 参考：https://en.wikipedia.org/wiki/List_of_file_signatures
    # 参考：https://www.garykessler.net/library/file_sigs.html
    (0, b"\xFF\xD8\xFF", "jpeg"),
    (0, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", "png"),
    (4, b"\x66\x74\x79\x70\x61\x76\x69\x66", "avif"),
    (4, b"\x66\x74\x79\x70\x68\x65\x69\x63", "heic"),
    (8, b"\x57\x45\x42\x50", "webp"),
    (4, b"\x66\x74\x79\x70\x4D\x53\x4E\x56", "mp4"),
    (4, b"\x66\x74\x79\x70\x69\x73\x6F\x6D", "mp4"),
    (4, b"\x66\x74\x79\x70\x6D\x70\x34\x32", "m4v"),
    (4, b"\x66\x74\x79\x70\x71\x74\x20\x20", "mov"),
    (0, b"\x1A\x45\xDF\xA3", "mkv"),
    (0, b"\x00\x00\x01\xB3", "mpg"),
    (0, b"\x00\x00\x01\xBA", "mpg"),
    (0, b"\x46\x4c\x56\x01", "flv"),
    (8, b"\x41\x56\x49\x20", "avi"),
)

FILE_SIGNATURES_LENGTH = max(offset + len(signature) for offset, signature, _ in FILE_SIGNATURES)
