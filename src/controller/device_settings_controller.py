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

        self.set_comboboxes()

    @event_bus.subscribe(EventEnum.OPEN_DEVICE_SETTINGS)
    def open_device_settings(self):
        self.view.deiconify()
        self.populate_comboboxes()

    def set_comboboxes(self):
        self.view.gantry_comport.set(self.model.get("gantry_port", default=""))
        self.view.pump_comport.set(self.model.get("pump_port", default=""))
        self.view.arduino_comport.set(
            self.model.get("arduino_port", default="")
        )
        self.view.camera_source.delete(0, "end")
        source = self.model.get("camera_source", default="0")
        if source is None:
            source = "0"
        self.view.camera_source.insert(0, source)

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

        self.model.set("gantry_port", gantry_port)
        self.model.set("pump_port", pump_port)
        self.model.set("arduino_port", arduino_port)
        self.model.set("camera_source", camera_source)

        self.view.withdraw()
