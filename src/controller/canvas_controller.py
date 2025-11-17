from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.canvas_model import MCanvas
    from view.canvas_view import VCanvas


class CCanvas():
    def __init__(self, view: VCanvas, model: MCanvas):
        self.view = view

    def _on_canvas_click(self, x: int, y: int):
        print("click", x,y)

    def _on_canvas_drag(self, x: int, y: int):
        print("drag", x,y)

    def _on_canvas_release(self, x: int, y: int):
        print("release", x,y)