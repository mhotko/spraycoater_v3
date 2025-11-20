import queue
from threading import Thread
from typing import cast, TYPE_CHECKING
from util.base_mvc import BaseController, BaseModel, BaseView
from util.connection_enum import ConnectionState
from util.serial_type_enum import SerialType
from util.threading_events import stop_event

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
        Thread(target=self._camera_worker, daemon=True).start()

    def _gantry_worker(self):
        result = self.model.connect_gantry()
        self.connection_queue.put(result)

        while not stop_event.is_set():
            self.connection_queue.put(
                (
                    SerialType.GANTRY,
                    ConnectionState.CONNECTED
                    if self.model.gantry_manager.is_connected
                    else ConnectionState.DISCONNECTED,
                )
            )
            stop_event.wait(1)

    def _camera_worker(self):
        first_run = True
        while not stop_event.is_set():
            if not first_run:
                result = self.model.camera_connected
                self.connection_queue.put(
                    (
                        SerialType.CAMERA,
                        ConnectionState.CONNECTED
                        if result
                        else ConnectionState.DISCONNECTED,
                    )
                )
            stop_event.wait(1)
            first_run = False

    def poll_connection_queue(self):
        try:
            while True:
                serial_type, state = self.connection_queue.get_nowait()
                print(serial_type, state)
                if serial_type == SerialType.GANTRY:
                    print("Updating Gantry indicator")

                    if state == ConnectionState.CONNECTED:
                        self.view.gantry_indicator.connected()
                    elif state == ConnectionState.CONNECTING:
                        self.view.gantry_indicator.connecting()
                    else:
                        self.view.gantry_indicator.disconnected()
                    self.view.gantry_indicator.update()
                elif serial_type == SerialType.CAMERA:
                    print("Updating camera indicator")
                    if state == ConnectionState.CONNECTED:
                        self.view.camera_indicator.connected()
                    elif state == ConnectionState.CONNECTING:
                        self.view.camera_indicator.connecting()
                    else:
                        self.view.camera_indicator.disconnected()
                    self.view.camera_indicator.update()
        except queue.Empty:
            pass
        self.view.after(100, self.poll_connection_queue)
