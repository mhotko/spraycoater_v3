from __future__ import annotations
from typing import TYPE_CHECKING
from util.draw_utility import Point
if TYPE_CHECKING:
    from model.canvas_model import MCanvas
    from view.canvas_view import VCanvas


class CCanvas():
    def __init__(self, view: VCanvas, model: MCanvas):
        self.view = view
        self.model = model

    def _on_canvas_click(self, x: int, y: int):
        if self.model.is_resizing(Point(x, y)):
            start_point = self.model.start_point
            self.model.set_start_point(self.model.end_point)
            self.model.set_end_point(start_point)
        else:
            self.model.set_start_point(Point(x, y))
            self.model.set_end_point(Point(x+1, y+1))

    def _on_canvas_drag(self, x: int, y: int):
        self.model.set_end_point(Point(x, y))

    def _on_canvas_release(self, x: int, y: int):
        pass
    
    def _update_canvas(self):
        self.model.read_frame()

        frame = self.model.get_converted_frame()
        if frame is not None:
            self.view.update_image(frame)

        self.view.after(20, self._update_canvas)