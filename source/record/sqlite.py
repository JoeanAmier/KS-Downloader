from typing import TYPE_CHECKING
from asyncio import CancelledError
from contextlib import suppress
from aiosqlite import connect

if TYPE_CHECKING:
    from source.manager import Manager


class SQLite:
    def __init__(
        self,
        manager: "Manager",
        filename: str,
        db_name: str,
        key: list[str],
        name: list[str],
        type_: list[str],
    ):
        self.db_name = db_name
        self.file = manager.data.joinpath(filename)
        self.database = None
        self.cursor = None
        self.key = key
        self.name = name
        self.type_ = type_

    async def _connect_database(self):
        self.database = await connect(self.file)
        self.cursor = await self.database.cursor()
        await self.database.execute(f"""CREATE TABLE IF NOT EXISTS {self.db_name} (
                {",".join(f"{i} {j}" for i, j in zip(self.name, self.type_))}
                );""")
        await self.database.commit()

    async def update(self, data: dict) -> None:
        await self.database.execute(
            f"""REPLACE INTO {self.db_name} (
                {", ".join(self.name)}
                ) VALUES (
                {", ".join("?" for _ in data)}
                );""",
            self.__generate_values(data),
        )
        await self.database.commit()

    def __generate_values(self, data: dict) -> tuple:
        return tuple(str(data[i]) for i in self.key)

    async def __aenter__(self):
        await self._connect_database()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        with suppress(CancelledError):
            await self.cursor.close()
            await self.database.close()
