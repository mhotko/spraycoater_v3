import cv2
import threading
import time
import numpy.typing as npt
import numpy as np

from util.calibration_loader import CalibrationLoader


class CameraController:
    def __init__(self):
        self.capture_dimensions = (1280, 720)
        self.video_source = 0
        self.capture_flag_windows = cv2.CAP_DSHOW

        self.cap = cv2.VideoCapture(
            self.video_source, self.capture_flag_windows
        )

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_dimensions[0])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_dimensions[1])

        self.newcam_mtx, self.roi = cv2.getOptimalNewCameraMatrix(
            CalibrationLoader.cam_mtx,
            CalibrationLoader.dist,
            (self.capture_dimensions[0], self.capture_dimensions[1]),
            1,
            (self.capture_dimensions[0], self.capture_dimensions[1]),
        )
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(
            CalibrationLoader.cam_mtx,
            CalibrationLoader.dist,
            None,  # type: ignore
            self.newcam_mtx,
            (self.capture_dimensions[0], self.capture_dimensions[1]),
            cv2.CV_16SC2,
        )  # type: ignore

        self.frame = None
        self.ret = False
        self.running = True
        self.lock = threading.Lock()

        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

    def _update(self):
        while self.running:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                with self.lock:
                    self.ret = ret

                    undistorted = cv2.remap(
                        frame, self.mapx, self.mapy, cv2.INTER_LINEAR
                    )

                    x, y, w_roi, h_roi = self.roi

                    undistorted_cropped = undistorted[
                        y:, x + 300 : x + w_roi - 300
                    ]
                    self.frame = undistorted_cropped
                if not ret:
                    time.sleep(0.01)
            else:
                self.frame = np.zeros(shape=(645, 567, 3), dtype=np.uint8)

    def read(self) -> tuple[bool, npt.NDArray | None]:
        with self.lock:
            if not self.cap.isOpened():
                return True, self.frame
            if self.frame is not None:
                return self.ret, self.frame
            else:
                return False, None
