from __future__ import annotations
from abc import ABC, abstractmethod


class BaseModel(ABC):
    pass


class BaseController(ABC):
    def __init__(self, view: BaseView, model: BaseModel) -> None:
        pass


class BaseView(ABC):
    @abstractmethod
    def set_controller(self, controller: BaseController) -> None:
        pass
