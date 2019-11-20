from collections.abc import Iterable
from unittest import TestCase
from unittest.mock import Mock

from omwp import OMWPApplication
from services.results import OMWPHandlerResult200, OMWPHandlerResult


class OMWPApplicationTest(TestCase):
    def setUp(self) -> None:
        self.omwp = OMWPApplication()
        self.start_response = Mock()
        self.environ = {}

    def test_callable_with_environ_and_start_response_args(self) -> None:
        self.omwp(self.environ, self.start_response)

    def test_response_byte_strings(self) -> None:
        result = self.omwp(self.environ, self.start_response)
        self.assertIsInstance(result, list)
        for item in result:
            self.assertIsInstance(item, bytes)

    def test_call_start_response(self) -> None:
        self.omwp(self.environ, self.start_response)
        self.start_response.assert_called()

    def test_call_start_response_with_str_and_iterable_params(self) -> None:
        def start_response_check_args(*args):
            self.assertGreaterEqual(len(args), 2)
            self.assertIsInstance(args[0], str)
            self.assertIsInstance(args[1], Iterable)

        self.start_response.side_effect = start_response_check_args
        self.omwp(self.environ, self.start_response)

    def test_call_start_response_status_format(self) -> None:
        def start_response_check_status(status, *args):
            """ Check based on PEP-3333 requirements to status https://www.python.org/dev/peps/pep-3333/#specification-details"""
            splitted_status = status.split()
            self.assertGreaterEqual(len(splitted_status), 2)
            self.assertTrue(splitted_status[0].isnumeric())

        self.start_response.side_effect = start_response_check_status
        self.omwp(self.environ, self.start_response)

    def test_call_start_response_response_headers_format(self) -> None:
        def start_response_check_response_headers(_, response_headers, *args):
            """ Check based on PEP-3333 requirements to response_headers https://www.python.org/dev/peps/pep-3333/#specification-details"""
            self.assertGreaterEqual(len(response_headers), 1)  # At least one response header must be in omwp
            for response_header in response_headers:
                self.assertIsInstance(response_header, tuple)

        self.start_response.side_effect = start_response_check_response_headers
        self.omwp(self.environ, self.start_response)

    def test_route(self):
        def hello() -> OMWPHandlerResult:
            return OMWPHandlerResult200("Hello, World!")

        self.omwp.add_route("/hello", hello)

        self.environ['PATH_INFO'] = '/hello'
        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"Hello, World!"])

    def test_decorator_based_route(self):
        @self.omwp.route('/hello_decorator')
        def hello() -> OMWPHandlerResult:
            return OMWPHandlerResult200("Hello, Decorator World!")

        self.environ['PATH_INFO'] = '/hello_decorator'

        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"Hello, Decorator World!"])
