from tkinter import Label, Toplevel
from tkinter.ttk import Combobox, Frame, Spinbox, Button
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

        settings_frame = Frame(self)
        settings_frame.pack(pady=10)

        # GANTRY COMPORT
        label = Label(settings_frame, text="Gantry Port:")
        label.grid(row=0, column=0, padx=5, pady=5)
        self.gantry_comport = Combobox(settings_frame)
        self.gantry_comport.grid(row=0, column=1, padx=5, pady=5)

        # PUMP COMPORT
        label = Label(settings_frame, text="Pump Port:")
        label.grid(row=1, column=0, padx=5, pady=5)
        self.pump_comport = Combobox(settings_frame)
        self.pump_comport.grid(row=1, column=1, padx=5, pady=5)

        # ARDUINO COMPORT
        label = Label(settings_frame, text="Arduino Port:")
        label.grid(row=2, column=0, padx=5, pady=5)
        self.arduino_comport = Combobox(settings_frame)
        self.arduino_comport.grid(row=2, column=1, padx=5, pady=5)

        # CAMERA SOURCE
        label = Label(settings_frame, text="Camera Source:")
        label.grid(row=3, column=0, padx=5, pady=5)
        self.camera_source = Spinbox(settings_frame, from_=0, to=10)
        self.camera_source.grid(row=3, column=1, padx=5, pady=5)

        cb = Button(settings_frame, text="Close", command=self.withdraw)
        cb.grid(row=4, column=0, padx=5, pady=5)

        sb = Button(
            settings_frame,
            text="Save Settings",
            command=self.save_device_settings,
        )
        sb.grid(row=4, column=1, padx=5, pady=5)

        # close_button = Button(self, text="Close", command=self.withdraw)
        # close_button.pack(pady=10)
        self.controller: "CDeviceSettings | None" = None

    def set_controller(self, controller: BaseController) -> None:
        """
        Sets the controller
        """
        self.controller = cast("CDeviceSettings", controller)

    def save_device_settings(self):
        if self.controller:
            self.controller.save_device_settings()
