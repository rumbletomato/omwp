from typing import Callable

from globals import RequestInfo
from services.handlers import OMWPHandler404


class PathNode:
    def __init__(self,
                 pattern: str = '',
                 handler: Callable = None):
        if pattern.startswith('<') and pattern.endswith('>'):
            self.pattern = '*'
            self.name = pattern[1:-1]
        else:
            self.pattern = pattern
            self.name = pattern
        self.handler = handler
        self.children = {}

    def add_child(self, node):
        self.children[node.pattern] = node

    def get_child(self, pattern):
        child = self.children.get(pattern)

        if child is None:
            child = self.children.get('*')

        return child

    def bind_url(self, path: str, handler: Callable):
        path_patterns = path.split('/')[1:]
        if len(path_patterns) < 1:
            return

        parent_node = self

        for _ in range(len(path_patterns)):
            pattern = path_patterns.pop(0)

            node = parent_node.get_child(pattern)
            if node is None:
                node = PathNode(pattern)
                parent_node.add_child(node)
            parent_node = node

        parent_node.handler = handler

    def get_handler(self, path: str):
        request_info = RequestInfo.get_instance()
        parent_node = self

        path_patterns = path.split('/')[1:]
        if len(path_patterns) < 1:
            return parent_node.handler

        for _ in range(len(path_patterns)):
            pattern = path_patterns.pop(0)
            node = parent_node.get_child(pattern)
            if node is None:
                break

            if node.pattern == '*':
                request_info.params[node.name] = pattern

            parent_node = node

        return parent_node.handler


class OMWPRoutingService:
    def __init__(self) -> None:
        self.routing_map: PathNode = PathNode()

    def route(self, path: str, handler: Callable) -> None:
        if not isinstance(handler, Callable):
            raise TypeError("Must be callable object")

        self.routing_map.bind_url(path, handler)

    def get_handler(self, path: str) -> Callable:
        handler = self.routing_map.get_handler(path)

        if handler is None:
            handler = OMWPHandler404()

        return handler
