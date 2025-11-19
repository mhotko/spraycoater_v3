from printrun import printcore
from util.serial_managers.serial_manager_base import SerialManager


class GantryManager(SerialManager):
    def __init__(self, serial_number=""):
        super().__init__(serial_number)
        self.connection: printcore.printcore | None = None
        self.comport = self.seek_comport()

    @property
    def is_connected(self) -> bool:
        if self.connection is not None:
            return self.connection.online
        return False
