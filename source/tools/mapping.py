from pathlib import Path
from typing import TYPE_CHECKING

from ..translation import _
from .retry import retry_limited

if TYPE_CHECKING:
    from ..manager import Manager
    from ..module import Database


__all__ = ["Mapping"]


class Mapping:
    def __init__(
        self,
        manager: "Manager",
        database: "Database",
    ):
        self.console = manager.console
        self.root = manager.folder
        self.folder_mode = manager.folder_mode
        self.database = database
        self.switch = manager.author_archive

    async def update_cache(
        self,
        id_: str,
        alias: str,
    ):
        if not self.switch:
            return
        if (a := await self.has_mapping(id_)) and a != alias:
            self.__check_file(
                id_,
                alias,
                a,
            )
        await self.database.update_mapping_data(
            id_,
            alias,
        )

    async def has_mapping(self, id_: str) -> str:
        return d[0] if (d := await self.database.get_mapping_data(id_)) else ""

    def __check_file(
        self,
        id_: str,
        alias: str,
        old_alias: str,
    ):
        if not (old_folder := self.root.joinpath(f"{id_}_{old_alias}")).is_dir():
            self.console.info(
                _("{old_folder} 文件夹不存在，跳过处理").format(
                    old_folder=old_folder.name
                ),
            )
            return
        self.__rename_folder(
            old_folder,
            id_,
            alias,
        )
        self.__scan_file(
            id_,
            alias,
            old_alias,
        )

    def __rename_folder(
        self,
        old_folder: Path,
        id_: str,
        alias: str,
    ):
        new_folder = self.root.joinpath(f"{id_}_{alias}")
        self.__rename(
            old_folder,
            new_folder,
            _("文件夹"),
        )
        self.console.info(
            _("文件夹 {old_folder} 重命名为 {new_folder}").format(
                old_folder=old_folder.name, new_folder=new_folder.name
            ),
        )

    def __rename_works_folder(
        self,
        old_: Path,
        alias: str,
        old_alias: str,
    ) -> Path:
        if old_alias in old_.name:
            new_ = old_.parent / old_.name.replace(old_alias, alias, 1)
            self.__rename(
                old_,
                new_,
                _("文件夹"),
            )
            self.console.info(
                _("文件夹 {old_folder} 重命名为 {new_folder}").format(
                    old_folder=old_.name, new_folder=new_.name
                ),
            )
            return new_
        return old_

    def __scan_file(
        self,
        id_: str,
        alias: str,
        old_alias: str,
    ):
        root = self.root.joinpath(f"{id_}_{alias}")
        item_list = root.iterdir()
        if self.folder_mode:
            for f in item_list:
                if f.is_dir():
                    f = self.__rename_works_folder(
                        f,
                        alias,
                        old_alias,
                    )
                    files = f.iterdir()
                    self.__batch_rename(
                        f,
                        files,
                        alias,
                        old_alias,
                    )
        else:
            self.__batch_rename(
                root,
                item_list,
                alias,
                old_alias,
            )

    def __batch_rename(
        self,
        root: Path,
        files,
        alias: str,
        old_alias: str,
    ):
        for old_file in files:
            if old_alias not in old_file.name:
                break
            self.__rename_file(
                root,
                old_file,
                alias,
                old_alias,
            )

    def __rename_file(
        self,
        root: Path,
        old_file: Path,
        alias: str,
        old_alias: str,
    ):
        new_file = root.joinpath(old_file.name.replace(old_alias, alias, 1))
        self.__rename(
            old_file,
            new_file,
            _("文件"),
        )
        self.console.info(
            _("文件 {old_file} 重命名为 {new_file}").format(
                old_file=old_file.name, new_file=new_file.name
            ),
        )
        return True

    @retry_limited
    def __rename(
        self,
        old_: Path,
        new_: Path,
        type_=_("文件"),
    ) -> bool:
        try:
            old_.rename(new_)
            return True
        except PermissionError as e:
            self.console.error(
                _("{type} {old}被占用，重命名失败: {error}").format(
                    type=type_, old=old_.name, error=e
                ),
            )
            return False
        except FileExistsError as e:
            self.console.error(
                _("{type} {new}名称重复，重命名失败: {error}").format(
                    type=type_, new=new_.name, error=e
                ),
            )
            return False
        except OSError as e:
            self.console.error(
                _("处理{type} {old}时发生预期之外的错误: {error}").format(
                    type=type_, old=old_.name, error=e
                ),
            )
            return True
