from util.db_manager import DBManager
from util.base_mvc import BaseModel
from util.connection_enum import ConnectionState
from util.event_type_enum import EventEnum
from util.serial_managers.arduino_manager import ArduinoManager
from util.serial_managers.gantry_manager import GantryManager
from util.event_bus_service import event_bus

from util.serial_type_enum import SerialType


class MConnection(BaseModel):
    def __init__(self, db_manager: DBManager) -> None:
        super().__init__()
        self.db_manager = db_manager
        self.gantry_manager = GantryManager()
        self.arduino_manager = ArduinoManager()
        self.camera_connected: bool = False
        self.bus = event_bus
        self.bus.register(self)

        self.set_gantry_comport()
        self.set_arduino_comport()

    def connect_gantry(self) -> tuple[SerialType, ConnectionState]:
        self.gantry_manager.connect()
        if self.gantry_manager.is_connected:
            return (SerialType.GANTRY, ConnectionState.CONNECTED)
        return (SerialType.GANTRY, ConnectionState.DISCONNECTED)

    def connect_arduino(self) -> tuple[SerialType, ConnectionState]:
        self.arduino_manager.connect()
        if self.arduino_manager.is_connected:
            return (SerialType.ARDUINO, ConnectionState.CONNECTED)
        return (SerialType.ARDUINO, ConnectionState.DISCONNECTED)

    def get(self, key: str, default="") -> str:
        row = self.db_manager.query_one(
            "SELECT value FROM device_settings WHERE key=?", (key,)
        )
        return row[0] if row else default

    def set_gantry_comport(self):
        comport = self.get("gantry_port", default="")
        self.gantry_manager.set_comport(comport)

    def set_arduino_comport(self):
        comport = self.get("arduino_port", default="")
        self.arduino_manager.set_comport(comport)
        print(f"Arduino comport set to: {comport}")

    @event_bus.subscribe(EventEnum.CAMERA_CONNECTION_STATE)
    def connect_camera(self, data: bool):
        self.camera_connected = data

    @event_bus.subscribe(EventEnum.DEVICE_SETTINGS_SAVED)
    def on_device_settings_saved(self):
        self.set_gantry_comport()
        self.gantry_manager.connect()
        self.set_arduino_comport()
        self.arduino_manager.connect()
