from __future__ import annotations
import tkinter as tk

from controller.canvas_controller import CCanvas
from model.canvas_model import MCanvas
from view.canvas_view import VCanvas

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SprayCoater GUI")

        canvas_model = MCanvas()
        canvas_view = VCanvas(self)
        canvas_controller = CCanvas(canvas_view, canvas_model)
        canvas_view.set_controller(canvas_controller)

        canvas_view.pack(side=tk.TOP, fill=tk.X)


if __name__ == "__main__":
    app: tk.Tk = App()
    app.mainloop()
