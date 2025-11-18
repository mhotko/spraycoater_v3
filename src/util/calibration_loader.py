from dataclasses import dataclass
import numpy as np

@dataclass
class CalibrationLoader:
    # savedir = "/home/ecat/Desktop/calibrations/"
    savedir = "./calibrations_v2/"
    cam_mtx=np.load(savedir+'cam_mtx_3.npy')
    dist=np.load(savedir+'dist_3.npy')
    rvec = np.load(savedir + 'rvecs_3.npy')
    tvec = np.load(savedir + 'tvecs_3.npy')

    # cam_mtx[0][0] = cam_mtx[0][0]
    # cam_mtx[1][1] = cam_mtx[1][1]
    # cam_mtx[0][2] = cam_mtx[0][2]
    # cam_mtx[1][2] = cam_mtx[1][2]

    # newcam_mtx=np.load(savedir+'newcam_mtx.npy')
    # newcam_mtx[0][0] = newcam_mtx[0][0]
    # newcam_mtx[1][1] = newcam_mtx[1][1]
    # newcam_mtx[0][2] = newcam_mtx[0][2]
    # newcam_mtx[1][2] = newcam_mtx[1][2]
    #
    # roi=np.load(savedir+'roi.npy')
    # rvec1=np.load(savedir+'rvec1.npy')
    # rvec1= rvec1
    # tvec1=np.load(savedir+'tvec1.npy')
    # tvec1 = tvec1
    # R_mtx=np.load(savedir+'R_mtx.npy')
    # R_mtx = R_mtx
    # Rt=np.load(savedir+'Rt.npy')
    # Rt = Rt
    # P_mtx=np.load(savedir+'P_mtx.npy')
    # P_mtx = P_mtx
    # s_arr=np.load(savedir+'s_arr.npy')
    # scalingfactor=s_arr[0]
    #
    # inverse_newcam_mtx = np.linalg.inv(newcam_mtx)
    # inverse_R_mtx = np.linalg.inv(R_mtx)