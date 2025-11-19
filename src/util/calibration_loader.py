from dataclasses import dataclass
import numpy as np


@dataclass
class CalibrationLoader:
    savedir = "./calibrations_v2/"
    cam_mtx = np.load(savedir + "cam_mtx_3.npy")
    dist = np.load(savedir + "dist_3.npy")
    rvec = np.load(savedir + "rvecs_3.npy")
    tvec = np.load(savedir + "tvecs_3.npy")
