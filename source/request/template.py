from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from source.manager import Manager


class API:
    def __init__(self, manager: "Manager"):
        self.session = manager.session
        self.headers = manager.pc_data_headers

    def run(self):
        pass

    def get_data(self):
        pass
