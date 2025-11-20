from typing import TYPE_CHECKING, cast
from util.base_mvc import BaseController, BaseModel, BaseView
from util.event_type_enum import EventEnum
from util.event_bus_service import event_bus

if TYPE_CHECKING:
    from view.device_settings_view import VDeviceSettings
    from model.device_settings_model import MDeviceSettings


class CDeviceSettings(BaseController):
    def __init__(
        self,
        view: BaseView,
        model: BaseModel,
    ):
        super().__init__(view, model)
        self.model = cast("MDeviceSettings", model)
        self.view = cast("VDeviceSettings", view)

        self.view.withdraw()
        self.event_bus = event_bus
        self.event_bus.register(self)

    @event_bus.subscribe(EventEnum.OPEN_DEVICE_SETTINGS)
    def open_device_settings(self):
        self.view.deiconify()
        self.populate_comboboxes()

    def populate_comboboxes(self):
        port_list = self.model.refresh_available_ports()
        self.view.gantry_comport["values"] = port_list
        self.view.pump_comport["values"] = port_list
        self.view.arduino_comport["values"] = port_list

    def save_device_settings(self):
        gantry_port = self.view.gantry_comport.get()
        pump_port = self.view.pump_comport.get()
        arduino_port = self.view.arduino_comport.get()
        camera_source = self.view.camera_source.get()

        print("Saving Device Settings:")
        print(f"Gantry Port: {gantry_port}")
        print(f"Pump Port: {pump_port}")
        print(f"Arduino Port: {arduino_port}")
        print(f"Camera Source: {camera_source}")

        self.view.withdraw()
