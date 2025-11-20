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
        # self.view.mainloop()
