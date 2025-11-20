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
    def __init__(self):
        super().__init__()
        self.device_settings = DeviceSettingsData(
            gantry_port="",
            pump_port="",
            arduino_port="",
            camera_source=0,
        )

    def refresh_available_ports(self) -> list[str]:
        return [port.device for port in list_ports.comports()]
