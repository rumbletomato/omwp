from collections.abc import Callable
from unittest import TestCase

from services.results import OMWPHandlerResult200, OMWPHandlerResult
from services.routing import OMWPRoutingService


class OMWPRoutingServiceTest(TestCase):
    def setUp(self) -> None:
        self.routing_service = OMWPRoutingService()

    def test_route_func(self):
        def hello() -> OMWPHandlerResult:
            return OMWPHandlerResult200("Hello, World!")

        self.routing_service.route("/hello", hello)

        handler = self.routing_service.get_handler('/hello')
        self.assertEqual(handler, hello)

        result = handler()
        self.assertIsInstance(result, OMWPHandlerResult)

    def test_get_callable_handler(self):
        handler = self.routing_service.get_handler("/some_handler")
        self.assertIsInstance(handler, Callable)

    def test_not_callable_route(self):
        with self.assertRaises(TypeError):
            self.routing_service.route("/hello", b"Hello, World!")
