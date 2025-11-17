from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

if TYPE_CHECKING:
    from controller.canvas_controller import CCanvas

class VCanvas(tk.Canvas):
    def __init__(self, parent: tk.Tk, height: int = 645, width: int = 567):
        super().__init__(parent, cursor="crosshair")

        self.height: int = height
        self.width: int = width

        self.config(height= self.height, width=self.width)

        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

        self.controller: CCanvas | None = None


    def set_controller(self, controller: CCanvas) -> None:
        """
        Sets the controller
        """
        self.controller = controller

    def _on_click(self, event: tk.Event) -> None:
        if self.controller:
            self.controller._on_canvas_click(event.x, event.y)
    
    def _on_drag(self, event: tk.Event) -> None:
        if self.controller:
            self.controller._on_canvas_drag(event.x, event.y)

    def _on_release(self, event: tk.Event) -> None:
        if self.controller:
            self.controller._on_canvas_release(event.x, event.y)