from enum import Enum, auto


class EventEnum(Enum):
    CAMERA_CONNECTION_STATE = auto()

    CASCADE = auto()
    MOVE_Y_220 = auto()
    RESET_POSITION = auto()
    CENTER_X = auto()
    CENTER_Y = auto()
    CENTER_XY = auto()
    HOME_X = auto()
    HOME_Y = auto()
    HOME_Z = auto()
    HOME_XYZ = auto()
    T_100 = auto()
    T_75 = auto()
    T_50 = auto()
    T_25 = auto()
    T_0 = auto()
    OPEN_SETTINGS = auto()
    OPEN_DEVICE_SETTINGS = auto()
