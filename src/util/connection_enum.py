from enum import Enum, auto


class ConnectionState(Enum):
    CONNECTED = auto()
    CONNECTING = auto()
    DISCONNECTED = auto()
