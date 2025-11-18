from util.camera_controller import CameraController
from PIL import Image, ImageTk
import cv2
import numpy.typing as npt

from util.draw_utility import DrawHandler, Point

class MCanvas():
    def __init__(self):
        self.camera_controller = CameraController()
        self.raw_frame: npt.NDArray | None = None
        self.converted_frame: ImageTk.PhotoImage | None = None
        self.start_point: Point = Point(-1, -1)
        self.end_point: Point = Point(-1, -1)
        self.draw_utility = DrawHandler()

    def read_frame(self) -> ImageTk.PhotoImage | None:
        ret, frame = self.camera_controller.read()
        if not ret or frame is None:
            return None
        self.raw_frame = frame.copy()
        self.draw()
    
    def get_converted_frame(self):
        if self.raw_frame is None:
            return
        rgb_image = cv2.cvtColor(self.raw_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_image)
        self.converted_frame = ImageTk.PhotoImage(image=img)
        return self.converted_frame
    
    def set_start_point(self, start_point: Point):
        self.start_point = start_point

    def set_end_point(self, end_point: Point):
        self.end_point = end_point

    def draw(self):
        if self.raw_frame is not None:
            
            self.raw_frame = self.draw_utility.draw(self.raw_frame, self.start_point, self.end_point)
    
    def is_resizing(self, click: Point) -> bool:
        return self.draw_utility.is_resizeing(click)