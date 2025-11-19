from util.base_mvc import BaseModel
from util.serial_managers.gantry_manager import GantryManager


class MConnection(BaseModel):
    def __init__(self) -> None:
        super().__init__()

        self.gantry_manager = GantryManager()
