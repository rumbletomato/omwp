from services.results import OMWPHandlerResult404


class OMWPHandler404:
    def __init__(self) -> None:
        self.result: OMWPHandlerResult404 = OMWPHandlerResult404()

    def __call__(self) -> OMWPHandlerResult404:
        return self.result
