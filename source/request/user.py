from typing import TYPE_CHECKING

from .template import API

if TYPE_CHECKING:
    from source.manager import Manager


class User(API):

    def __init__(self, manager: "Manager"):
        super().__init__(manager)

    def run(self):
        pass

    def get_data(self):
        pass
