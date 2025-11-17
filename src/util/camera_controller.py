import cv2
import threading
import time

class CameraController:
    def __init__(self):
        self.capture_dimensions = (1280, 720)
        self.video_source = 0
        self.capture_flag_windows = cv2.CAP_DSHOW

        self.cap = cv2.VideoCapture(self.video_source, self.capture_flag_windows)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_dimensions[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_dimensions[1])

        self.frame = None
        self.ret = False
        self.running = True
        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
    
    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            with self.lock:
                self.ret = ret

                # undistorted = cv2.remap(frame, self.mapx, self.mapy, cv2.INTER_LINEAR)
                # x, y, w_roi, h_roi = self.roi
                # undistorted_cropped = undistorted[y:, x + 300:x + w_roi - 300]
                self.frame = frame
            if not ret:
                time.sleep(0.01)
    
    def read(self):
        with self.lock:
            if self.frame is not None:
                return self.ret, self.frame
            else:
                return False, None