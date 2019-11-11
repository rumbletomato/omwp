from typing import Callable, List

from services.results import OMWPHandlerResult
from services.routing import OMWPRoutingService


class OMWPApplication:
    def __init__(self) -> None:
        self.routing_service = OMWPRoutingService()

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
        path = environ['PATH_INFO']
        handler = self.routing_service.get_handler(path)

        result: OMWPHandlerResult = handler()
        start_response(result.status, [('content-type', 'text/plain')])

        return [result.payload]

    def route(self, path: str, handler: Callable) -> None:
        self.routing_service.route(path, handler)
