from typing import cast, TYPE_CHECKING
from util.base_mvc import BaseController, BaseModel, BaseView

if TYPE_CHECKING:
    from view.connection_view import VConection
    from model.connection_model import MConnection


class CConnection(BaseController):
    def __init__(self, view: BaseView, model: BaseModel):
        super().__init__(view, model)
        self.view = cast("VConection", view)
        self.model = cast("MConnection", model)
