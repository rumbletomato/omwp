from collections.abc import Callable
from unittest import TestCase
from unittest.mock import Mock

from globals import RequestInfo
from omwp import OMWPApplication
from services.results import OMWPHandlerResult200, OMWPHandlerResult
from services.routing import OMWPRoutingService


class OMWPRoutingServiceTest(TestCase):
    def setUp(self) -> None:
        self.omwp = OMWPApplication()
        self.start_response = Mock()
        self.environ = {}

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

    def test_get_path_param_handler(self):
        @self.omwp.route('/hello/<username>')
        def hello_username() -> OMWPHandlerResult:
            request_info = RequestInfo.get_instance()

            username = request_info.params.get('username')
            return OMWPHandlerResult200(f'Hello, {username}!')

        self.environ['PATH_INFO'] = '/hello/stranger'

        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"Hello, stranger!"])
