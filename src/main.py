from __future__ import annotations
from os import environ
from pathlib import Path
from sys import base_prefix
import tkinter as tk
from tkinter import font, Tk

from controller.canvas_controller import CCanvas
from controller.connection_controller import CConnection
from model.canvas_model import MCanvas
from model.connection_model import MConnection
from view.canvas_view import VCanvas
from view.connection_view import VConection

environ["TCL_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tcl8.6")
environ["TK_LIBRARY"] = str(Path(base_prefix) / "tcl" / "tk8.6")


class App(Tk):
    def __init__(self):
        super().__init__()

        self.title("Spraycoater GUI")

        self.defaultFont = font.nametofont("TkDefaultFont")
        self.defaultFont.configure(family="Arial", size=12, weight=font.BOLD)

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


if __name__ == "__main__":
    app: tk.Tk = App()
    app.mainloop()
