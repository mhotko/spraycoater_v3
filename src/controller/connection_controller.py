import queue
from threading import Thread
from typing import cast, TYPE_CHECKING
from util.base_mvc import BaseController, BaseModel, BaseView
from util.connection_enum import ConnectionState
from util.serial_type_enum import SerialType

if TYPE_CHECKING:
    from view.connection_view import VConection
    from model.connection_model import MConnection


class CConnection(BaseController):
    def __init__(self, view: BaseView, model: BaseModel):
        super().__init__(view, model)
        self.view = cast("VConection", view)
        self.model = cast("MConnection", model)

        self.connection_queue: queue.Queue[
            tuple[SerialType, ConnectionState]
        ] = queue.Queue()

        self.poll_connection_queue()
        self.start_connection_process()

    def start_connection_process(self):
        Thread(target=self._gantry_worker, daemon=True).start()

    def _gantry_worker(self):
        result = self.model.connect_gantry()
        self.connection_queue.put(result)

    def poll_connection_queue(self):
        try:
            while True:
                serial_type, state = self.connection_queue.get_nowait()
                if serial_type == SerialType.GANTRY:
                    if state == ConnectionState.CONNECTED:
                        self.view.gantry_indicator.connected()
                    elif state == ConnectionState.CONNECTING:
                        self.view.gantry_indicator.connecting()
                    else:
                        self.view.gantry_indicator.disconnected()
                    self.view.gantry_indicator.update()
        except queue.Empty:
            pass
        self.view.after(100, self.poll_connection_queue)
