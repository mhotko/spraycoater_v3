from abc import ABC, abstractmethod
from serial.tools import list_ports


class SerialManager(ABC):
    def __init__(self, serial_number: str):
        super().__init__()
        self._serial_number = serial_number

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass

    def seek_comport(self) -> str:
        ports = list(list_ports.comports())
        for p in ports:
            if p.serial_number == self._serial_number:
                return p.device
        else:
            return ""
