from util.base_mvc import BaseController, BaseModel, BaseView


class CConnection(BaseController):
    def __init__(self, view: BaseView, model: BaseModel):
        super().__init__(view, model)
