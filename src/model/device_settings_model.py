from util.db_manager import DBManager
from util.base_mvc import BaseModel
from serial.tools import list_ports
from dataclasses import dataclass


@dataclass
class DeviceSettingsData:
    gantry_port: str
    pump_port: str
    arduino_port: str
    camera_source: int


class MDeviceSettings(BaseModel):
    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.device_settings = DeviceSettingsData(
            gantry_port="",
            pump_port="",
            arduino_port="",
            camera_source=0,
        )

        self.db_manager = db_manager
        self._init_table()

    def _init_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS device_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        """
        self.db_manager.execute_query(create_table_query)

    def set(self, key: str, value: str):
        self.db_manager.execute_query(
            """
            INSERT OR IGNORE INTO device_settings(key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """,
            (key, value),
        )

    def get(self, key: str, default=None) -> str | None:
        row = self.db_manager.query_one(
            "SELECT value FROM device_settings WHERE key=?", (key,)
        )
        return row[0] if row else default

    def all(self):
        return self.db_manager.query_all(
            "SELECT key, value FROM device_settings"
        )

    def refresh_available_ports(self) -> list[str]:
        return [port.device for port in list_ports.comports()]
