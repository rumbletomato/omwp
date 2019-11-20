from typing import Callable, List

from services.results import OMWPHandlerResult
from services.routing import OMWPRoutingService


class OMWPApplication:
    def __init__(self) -> None:
        self.routing_service = OMWPRoutingService()

    def __call__(self, environ: dict, start_response: Callable) -> List[bytes]:
        path = environ.get('PATH_INFO', '')
        handler = self.routing_service.get_handler(path)

        result: OMWPHandlerResult = handler()
        start_response(result.status, [('content-type', 'text/plain')])

        return [result.payload]

    def add_route(self, path: str, handler: Callable) -> None:
        """
        Add route to application

        :param path: the URL as string
        :param handler: the callable object to handle request
        """
        self.routing_service.route(path, handler)

    def route(self, path: str) -> Callable:
        """
        Decorator based routing

        :param path: the URL as string
        """

        def decorator(f):
            self.add_route(path, f)
            return f

        return decorator
