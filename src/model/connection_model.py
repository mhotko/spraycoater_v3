from util.base_mvc import BaseModel
from util.connection_enum import ConnectionState
from util.serial_managers.gantry_manager import GantryManager
import time

from util.serial_type_enum import SerialType


class MConnection(BaseModel):
    def __init__(self) -> None:
        super().__init__()

        self.gantry_manager = GantryManager()

    def connect_gantry(self) -> tuple[SerialType, ConnectionState]:
        i = 0
        while not self.gantry_manager.is_connected and i < 5:
            try:
                self.gantry_manager.connect()
                break
            except ConnectionError as e:
                print(f"Attempt {i + 1}: {e}")
                time.sleep(1)
            i += 1
        return (
            SerialType.GANTRY,
            ConnectionState.CONNECTED
            if self.gantry_manager.is_connected
            else ConnectionState.DISCONNECTED,
        )
