from __future__ import annotations
from os import environ
from pathlib import Path
from sys import base_prefix
import tkinter as tk
from tkinter import font, Tk
from controller.device_settings_controller import CDeviceSettings
from menu_bar import MenuBar
from model.device_settings_model import MDeviceSettings
from util.db_manager import DBManager
from util.threading_events import stop_event

from controller.canvas_controller import CCanvas
from controller.connection_controller import CConnection
from model.canvas_model import MCanvas
from model.connection_model import MConnection
from view.canvas_view import VCanvas
from view.connection_view import VConection
from view.device_settings_view import VDeviceSettings


environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")

DOCUMENTS = Path.home() / "Documents" / "SpraycoaterGUI"
if not DOCUMENTS.exists():
    DOCUMENTS.mkdir(parents=True, exist_ok=True)


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Spraycoater GUI")

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=12, weight=font.BOLD)

        self.protocol("WM_DELETE_WINDOW", self.window_close)

        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)

        self.db_file = Path(DOCUMENTS / "app_database.db")
        if not self.db_file.exists():
            self.db_file.touch()

        self.db_manager = DBManager(str(self.db_file))

        # CANVAS
        canvas_model = MCanvas()
        canvas_view = VCanvas(self)
        canvas_controller = CCanvas(canvas_view, canvas_model)
        canvas_view.set_controller(canvas_controller)
        canvas_controller._update_canvas()

        canvas_view.pack(side=tk.TOP, fill=tk.X)

        # CONNECTION
        connection_model = MConnection()
        connection_view = VConection(self)
        connection_controller = CConnection(connection_view, connection_model)
        connection_view.set_controller(connection_controller)

        connection_view.pack()

        # DEVICE SETTINGS
        device_settings_model = MDeviceSettings(self.db_manager)
        device_settings_view = VDeviceSettings(self)
        device_settings_controller = CDeviceSettings(
            device_settings_view, device_settings_model
        )
        device_settings_view.set_controller(device_settings_controller)

    def window_close(self):
        stop_event.set()
        self.destroy()


if __name__ == "__main__":
    app: tk.Tk = App()
    app.mainloop()
