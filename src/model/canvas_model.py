from util.camera_controller import CameraController
from PIL import Image, ImageTk
import cv2

class MCanvas():
    def __init__(self):
        self.camera_controller = CameraController()

    def read_frame(self) -> ImageTk.PhotoImage | None:
        ret, frame = self.camera_controller.read()
        if not ret or frame is None:
            return None
        
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_image)
        img_tk = ImageTk.PhotoImage(image=img)
        return img_tk