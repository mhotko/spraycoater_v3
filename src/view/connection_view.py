import tkinter as tk

from util.connection_enum import ConnectionState


class ConnectedIndicator:
    def __init__(self, parent: tk.Misc, text: str = "Default") -> None:
        self._parent = parent
        self._text = text
        self._state = ConnectionState.DISCONNECTED

        self._colors: dict[ConnectionState, str] = {
            ConnectionState.CONNECTED: "#27ae60",
            ConnectionState.CONNECTING: "#f1c40f",
            ConnectionState.DISCONNECTED: "#e74c3c",
        }

        self.canvas = tk.Canvas(
            parent, width=20, height=20, highlightthickness=0
        )
        self.canvas.pack(side="left", padx=(5, 2), pady=10)
        self.light = self.canvas.create_oval(
            2, 2, 18, 18, fill=self._colors[self._state]
        )

        self.status_label = tk.Label(parent, text=self._text)
        self.status_label.pack(side="left", padx=(0, 5), pady=10)

    def connected(self):
        self._state = ConnectionState.CONNECTED

    def connecting(self):
        self._state = ConnectionState.CONNECTING

    def disconnected(self):
        self._state = ConnectionState.DISCONNECTED

    def update(self):
        color = self._colors.get(
            self._state, self._colors[ConnectionState.DISCONNECTED]
        )
        self.canvas.itemconfig(self.light, fill=color)


class VCoonection(tk.Frame):
    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.parent = master
        self.pump_indicator = ConnectedIndicator(self.master, text="Pump")

        self.gantry_indicator = ConnectedIndicator(self.master, text="Gantry")

        self.camera_indicator = ConnectedIndicator(self.master, text="Camera")

        self.arduino_indicator = ConnectedIndicator(
            self.master, text="Arduino"
        )
