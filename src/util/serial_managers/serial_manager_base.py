from abc import ABC, abstractmethod


class SerialManager(ABC):
    def __init__(self, comport: str):
        super().__init__()
        self._comport = comport

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass
