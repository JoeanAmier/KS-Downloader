from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from ..manager import Manager


class User(API):
    def __init__(self, manager: "Manager"):
        super().__init__(manager)
