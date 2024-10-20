from .sqlite import SQLite


class RecordManager:
    detail = (
        ("collection_time", "采集日期", "TEXT"),
        ("photoType", "作品类型", "TEXT"),
        ("authorID", "作者ID", "TEXT"),
        ("name", "作者昵称", "TEXT"),
        ("userSex", "作者性别", "TEXT"),
        ("detailID", "作品ID", "TEXT PRIMARY KEY"),
        ("caption", "作品文案", "TEXT"),
        ("coverUrl", "封面地址", "TEXT"),
        ("duration", "视频时长", "TEXT"),
        ("realLikeCount", "点赞数量", "INTEGER"),
        ("shareCount", "分享数量", "INTEGER"),
        ("commentCount", "评论数量", "INTEGER"),
        ("timestamp", "发布日期", "TEXT"),
        ("viewCount", "浏览数量", "TEXT"),
        ("download", "下载地址", "TEXT"),
    )
    # detail = (
    #     ("collection_time", "采集日期", "TEXT"),
    #     ("photoType", "作品类型", "TEXT"),
    #     ("userName", "作者昵称", "TEXT"),
    #     ("userId", "作者ID", "TEXT"),
    #     ("userEid", "作者EID", "TEXT"),
    #     ("userSex", "性别", "TEXT"),
    #     ("headUrls", "头像链接", "TEXT"),
    #     ("fanCount", "粉丝数量", "INTEGER"),
    #     ("followCount", "关注数量", "INTEGER"),
    #     ("photoCount", "作品数量", "INTEGER"),
    #     ("timestamp", "发布日期", "TEXT"),
    #     ("detailID", "作品ID", "TEXT PRIMARY KEY"),
    #     ("duration", "作品时长", "TEXT"),
    #     ("caption", "作品文案", "TEXT"),
    #     ("height", "作品高度", "INTEGER"),
    #     ("width", "作品宽度", "INTEGER"),
    #     ("download", "下载链接", "TEXT"),
    #     ("coverUrls", "封面链接", "TEXT"),
    #     ("webpCoverUrls", "WEBP封面链接", "TEXT"),
    #     ("music_name", "音乐标题", "TEXT"),
    #     ("audioUrls", "音乐链接", "TEXT"),
    #     ("collectionCount", "收藏数量", "INTEGER"),
    #     ("commentCount", "评论数量", "INTEGER"),
    #     ("viewCount", "浏览数量", "INTEGER"),
    #     ("likeCount", "点赞数量", "INTEGER"),
    # )
    format = {
        "SQLite": SQLite,
    }
    type = {
        "detail": {
            "filename": "DetailData.db",
            "key": [i[0] for i in detail],
            "name": [i[1] for i in detail],
            "type_": [i[2] for i in detail],
        }
    }

    def run(self, type_="detail", format_="SQLite"):
        return self.format[format_], self.type[type_]
