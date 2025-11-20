from printrun import printcore
from util.serial_managers.serial_manager_base import SerialManager


class GantryManager(SerialManager):
    def __init__(self, comport=""):
        super().__init__(comport)
        self.connection: printcore.printcore | None = None
        self.comport = comport
        self.baudrate = 115200

    @property
    def is_connected(self) -> bool:
        if self.connection is not None:
            return self.connection.online
        return False

    def connect(self):
        if not self.is_connected:
            self.connection = printcore.printcore(self.comport, self.baudrate)
            if not self.is_connected:
                raise ConnectionError("Failed to connect to Gantry.")
        else:
            raise ConnectionError("Gantry is already connected.")
