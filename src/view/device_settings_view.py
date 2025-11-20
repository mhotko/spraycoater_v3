from tkinter import Label, Toplevel, Button
from typing import cast, TYPE_CHECKING

from util.base_mvc import BaseView, BaseController

if TYPE_CHECKING:
    from controller.device_settings_controller import CDeviceSettings


class VDeviceSettings(Toplevel, BaseView):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Device Settings")
        self.geometry("400x300")

        label = Label(self, text="Device Settings")
        label.pack(pady=20)

        close_button = Button(self, text="Close", command=self.withdraw)
        close_button.pack(pady=10)
        self.controller: "CDeviceSettings | None" = None

    def set_controller(self, controller: BaseController) -> None:
        """
        Sets the controller
        """
        self.controller = cast("CDeviceSettings", controller)
