from printrun import printcore
from util.serial_managers.serial_manager_base import SerialManager

import logging

logger = logging.getLogger(__name__)


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
                logger.error("Failed to connect to Gantry.")
        else:
            if self.connection is not None:
                self.connection.disconnect()
                self.connection = None
            self.connection = printcore.printcore(self.comport, self.baudrate)
            if not self.is_connected:
                logger.error("Failed to connect to Gantry.")

    def set_comport(self, comport: str):
        self.comport = comport
