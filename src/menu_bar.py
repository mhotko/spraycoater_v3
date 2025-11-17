from enum import Enum, auto
import tkinter as tk
from typing import Callable

class MenuItemEnum(Enum):
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

class MenuBar(tk.Menu):
    def __init__(self, master: tk.Tk, on_event: Callable[[MenuItemEnum], None], **kwargs):
        super().__init__(master, **kwargs)

        self._on_event: Callable[[MenuItemEnum], None] = on_event

        self._calibrate_parent_item: tk.Menu = tk.Menu(self, tearoff=0)
        self._gantry_parent_item: tk.Menu = tk.Menu(self, tearoff=0)
        self._settings_parent_item: tk.Menu = tk.Menu(self, tearoff=0)

        self._create_calibrate_menu()
        self._create_gantry_menu()
        self._create_settings_menu()

    def _create_calibrate_menu(self) -> None:
        self.add_cascade(label="Calibrate", menu=self._calibrate_parent_item)
        self._calibrate_parent_item.add_command(
            label="Calibrate", command=lambda: self._on_event(MenuItemEnum.CASCADE))

    def _create_gantry_menu(self) -> None:
        self.add_cascade(label="Gantry", menu=self._gantry_parent_item)
        self._gantry_parent_item.add_command(
            label="Move Y=220", command=lambda: self._on_event(MenuItemEnum.MOVE_Y_220))

        self._gantry_parent_item.add_separator()
        self._create_gantry_move_menu()
        self._create_gantry_home_menu()
        self._create_gantry_temp_menu()

    def _create_gantry_move_menu(self) -> None:

        gantry_move_menu: tk.Menu = tk.Menu(self._gantry_parent_item, tearoff=0)
        self._gantry_parent_item.add_cascade(
            label="Move", menu=gantry_move_menu)
        gantry_move_menu.add_command(
            label="Reset Position", command=lambda: self._on_event(MenuItemEnum.RESET_POSITION))
        gantry_move_menu.add_command(
            label="Center X", command=lambda: self._on_event(MenuItemEnum.CENTER_X))
        gantry_move_menu.add_command(
            label="Center Y", command=lambda: self._on_event(MenuItemEnum.CENTER_Y))
        gantry_move_menu.add_command(
            label="Center XY", command=lambda: self._on_event(MenuItemEnum.CENTER_XY))

    def _create_gantry_home_menu(self) -> None:

        gantry_home_menu: tk.Menu = tk.Menu(self._gantry_parent_item, tearoff=0)
        self._gantry_parent_item.add_cascade(
            label="Home", menu=gantry_home_menu)
        gantry_home_menu.add_command(
            label="Home X", command=lambda: self._on_event(MenuItemEnum.HOME_X))
        gantry_home_menu.add_command(
            label="Home Y", command=lambda: self._on_event(MenuItemEnum.HOME_Y))
        gantry_home_menu.add_command(
            label="Home Z", command=lambda: self._on_event(MenuItemEnum.HOME_Z))
        gantry_home_menu.add_command(
            label="Home XYZ", command=lambda: self._on_event(MenuItemEnum.HOME_XYZ))

    def _create_gantry_temp_menu(self) -> None:
        gantry_temp_menu: tk.Menu = tk.Menu(self._gantry_parent_item, tearoff=0)
        self._gantry_parent_item.add_cascade(
            label="Temperature", menu=gantry_temp_menu)
        gantry_temp_menu.add_command(
            label="Set 100", command=lambda: self._on_event(MenuItemEnum.T_100))
        gantry_temp_menu.add_command(
            label="Set 75", command=lambda: self._on_event(MenuItemEnum.T_75))
        gantry_temp_menu.add_command(
            label="Set 50", command=lambda: self._on_event(MenuItemEnum.T_50))
        gantry_temp_menu.add_command(
            label="Set 25", command=lambda: self._on_event(MenuItemEnum.T_25))
        gantry_temp_menu.add_command(
            label="Set Off", command=lambda: self._on_event(MenuItemEnum.T_0))

    def _create_settings_menu(self) -> None:
        self.add_cascade(label='Settings', menu=self._settings_parent_item)
        self._settings_parent_item.add_command(
            label='Open settings', command=lambda: self._on_event(MenuItemEnum.OPEN_SETTINGS))
