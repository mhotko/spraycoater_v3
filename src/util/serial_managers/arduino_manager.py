import serial
from util.serial_managers.serial_manager_base import SerialManager

import logging

logger = logging.getLogger(__name__)


class ArduinoManager(SerialManager):
    def __init__(self, comport=""):
        super().__init__(comport)
        self.connection: serial.Serial | None = None
        self.comport = comport
        self.baudrate = 9600

    @property
    def is_connected(self) -> bool:
        if self.connection is not None:
            return self.connection.is_open
        return False

    def connect(self):
        if not self.is_connected:
            try:
                self.connection = serial.Serial(self.comport, self.baudrate)
                if not self.is_connected:
                    logger.error("Failed to connect to Arduino.")
            except serial.SerialException:
                logger.error("Failed to connect to Arduino.")
        else:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
            try:
                self.connection = serial.Serial(self.comport, self.baudrate)
                if not self.is_connected:
                    logger.error("Failed to connect to Arduino.")
            except serial.SerialException:
                logger.error("Failed to connect to Arduino.")

    def set_comport(self, comport: str):
        self.comport = comport
