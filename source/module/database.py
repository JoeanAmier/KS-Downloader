from typing import TYPE_CHECKING
from asyncio import CancelledError
from contextlib import suppress
from aiosqlite import Row, connect

from ..static import PROJECT_ROOT

if TYPE_CHECKING:
    from ..manager import Manager


class Database:
    record = 1
    __FILE = "KS-Downloader.db"

    def __init__(
        self,
        manager: "Manager",
    ):
        self.file = PROJECT_ROOT.joinpath(self.__FILE)
        self.switch = manager.author_archive
        self.database = None
        self.cursor = None

    async def __connect_database(self):
        self.database = await connect(self.file)
        self.database.row_factory = Row
        self.cursor = await self.database.cursor()
        await self.__create_table()
        await self.__write_default_config()
        await self.__write_default_option()
        await self.database.commit()

    async def __create_table(self):
        await self.database.execute(
            "CREATE TABLE IF NOT EXISTS download_data (ID TEXT PRIMARY KEY);"
        )
        await self.database.execute(
            """CREATE TABLE IF NOT EXISTS config_data (
            NAME TEXT PRIMARY KEY,
            VALUE INTEGER NOT NULL CHECK(VALUE IN (0, 1))
            );"""
        )
        await self.database.execute("""CREATE TABLE IF NOT EXISTS option_data (
                NAME TEXT PRIMARY KEY,
                VALUE TEXT NOT NULL
                );""")
        await self.database.execute(
            "CREATE TABLE IF NOT EXISTS mapping_data ("
            "ID TEXT PRIMARY KEY,"
            "NAME TEXT NOT NULL"
            ");"
        )

    async def __write_default_config(self):
        await self.database.execute("""INSERT OR IGNORE INTO config_data (NAME, VALUE)
                            VALUES ('Record', 1),
                            ('Disclaimer', 0);""")

    async def __write_default_option(self):
        await self.database.execute("""INSERT OR IGNORE INTO option_data (NAME, VALUE)
                            VALUES ('Language', 'zh_CN');""")

    async def __read_config_data(self):
        await self.cursor.execute("SELECT * FROM config_data")
        return await self.cursor.fetchall()

    async def __read_option_data(self):
        await self.cursor.execute("SELECT * FROM option_data")
        return await self.cursor.fetchall()

    @staticmethod
    def __format_config(config: list) -> dict:
        return {i["NAME"]: i["VALUE"] for i in config}

    async def read_config(
        self,
    ) -> dict:
        config = await self.__read_config_data()
        config = self.__format_config(config)
        self.record = config["Record"]
        return config

    async def read_option(
        self,
    ) -> dict:
        option = await self.__read_option_data()
        option = self.__format_config(option)
        return option

    async def update_config_data(
        self,
        name: str,
        value: int,
    ):
        await self.database.execute(
            "REPLACE INTO config_data (NAME, VALUE) VALUES (?,?)", (name, value)
        )
        await self.database.commit()

    async def update_option_data(
        self,
        name: str,
        value: str,
    ):
        await self.database.execute(
            "REPLACE INTO option_data (NAME, VALUE) VALUES (?,?)", (name, value)
        )
        await self.database.commit()

    async def has_download_data(self, id_: str) -> bool:
        if not self.record:
            return False
        await self.cursor.execute("SELECT ID FROM download_data WHERE ID=?", (id_,))
        return bool(await self.cursor.fetchone())

    async def write_download_data(self, id_: str):
        if self.record:
            await self.database.execute(
                "INSERT OR IGNORE INTO download_data (ID) VALUES (?);", (id_,)
            )
            await self.database.commit()

    async def delete_download_data(self, ids: list | tuple | str):
        if not self.record:
            return
        if isinstance(ids, str):
            ids = [ids]
        [await self.__delete_download_data(i) for i in ids]
        await self.database.commit()

    async def __delete_download_data(self, id_: str):
        await self.database.execute("DELETE FROM download_data WHERE ID=?", (id_,))

    async def delete_all_download_data(self):
        await self.database.execute("DELETE FROM download_data")
        await self.database.commit()

    async def get_mapping_data(self, id_: str):
        if self.switch:
            await self.cursor.execute(
                "SELECT NAME FROM mapping_data WHERE ID=?", (id_,)
            )
            return await self.cursor.fetchone()

    async def update_mapping_data(
        self,
        id_: str,
        name: str,
    ) -> None:
        if self.switch:
            await self.database.execute(
                "REPLACE INTO mapping_data VALUES (?, ?);",
                (
                    id_,
                    name,
                ),
            )
            await self.database.commit()

    async def __aenter__(self):
        await self.__connect_database()
        return self

    async def close(self):
        with suppress(CancelledError):
            await self.cursor.close()
        await self.database.close()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close()
