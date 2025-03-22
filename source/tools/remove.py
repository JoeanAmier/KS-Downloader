from contextlib import suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


def remove_empty_directories(path: "Path") -> None:
    exclude = {
        "\\.",
        "\\_",
        "\\__",
    }
    for dir_path, dir_names, file_names in path.walk(
        top_down=False,
    ):
        if any(i in str(dir_path) for i in exclude):
            continue
        if not dir_names and not file_names:
            with suppress(OSError):
                dir_path.rmdir()
