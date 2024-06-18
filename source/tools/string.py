def is_chinese_char(char):
    """判断一个字符是否是中文字符"""
    if "\u4e00" <= char <= "\u9fff":
        return True
    return False


def truncation(string: str, length=256) -> str:
    result = ""
    for s in string:
        result += s
        if is_chinese_char(s):
            length -= 2
        else:
            length -= 1
        if length < 1:
            break
    return result
