from util.base_mvc import BaseModel
from util.camera_grabber import CameraFrameGrabber
from PIL import Image, ImageTk
import cv2
import numpy.typing as npt

from util.draw_utility import DrawHandler, Point

from util.event_type_enum import EventEnum
from util.event_bus_service import event_bus
from util.db_manager import DBManager


class MCanvas(BaseModel):
    def __init__(self, db_manager: DBManager) -> None:
        super().__init__()
        self.db_manager = db_manager
        self.camera_controller = CameraFrameGrabber()
        # self.set_camera_source()
        self.raw_frame: npt.NDArray | None = None
        self.converted_frame: ImageTk.PhotoImage | None = None
        self.start_point: Point = Point(-1, -1)
        self.end_point: Point = Point(-1, -1)
        self.draw_utility = DrawHandler()
        self.event_bus = event_bus
        self.event_bus.register(self)

    def read_frame(self) -> ImageTk.PhotoImage | None:
        self.event_bus.publish(
            EventEnum.CAMERA_CONNECTION_STATE,
            data=self.camera_controller.cap.isOpened()
            if self.camera_controller.cap
            else False,
        )
        ret, frame = self.camera_controller.read()
        if not ret or frame is None:
            return None
        self.raw_frame = frame.copy()
        self.draw()

    def set_camera_source(self):
        source = self.get("camera_source", default="0")
        self.camera_controller.set_new_source(int(source))

    @event_bus.subscribe(EventEnum.CAMERA_SOURCE_CHANGED)
    def on_device_settings_saved(self):
        self.set_camera_source()

    def get(self, key: str, default="") -> str:
        row = self.db_manager.query_one(
            "SELECT value FROM device_settings WHERE key=?", (key,)
        )
        return row[0] if row else default

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
            self.raw_frame = self.draw_utility.draw(
                self.raw_frame, self.start_point, self.end_point
            )

    def is_resizing(self, click: Point) -> bool:
        return self.draw_utility.is_resizeing(click)
