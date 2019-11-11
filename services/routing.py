from typing import Callable, Dict

from services.handlers import OMWPHandler404


class OMWPRoutingService:
    def __init__(self) -> None:
        self.routing_map: Dict[str, Callable] = {}

    def route(self, path: str, handler: Callable) -> None:
        if not isinstance(handler, Callable):
            raise TypeError("Must be callable object")

        self.routing_map[path] = handler

    def get_handler(self, path: str) -> Callable:
        handler = self.routing_map.get(path, None)

        if handler is None:
            handler = OMWPHandler404()

        return handler
