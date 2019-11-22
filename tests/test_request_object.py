from unittest import TestCase
from unittest.mock import Mock

from omwp import OMWPApplication
from services.results import OMWPHandlerResult, OMWPHandlerResult200, OMWPHandlerResult500


class RequestObjectTest(TestCase):
    def setUp(self) -> None:
        self.omwp = OMWPApplication()
        self.start_response = Mock()
        self.environ = {}

    def test_path_info(self) -> None:
        @self.omwp.route('/hello')
        def hello() -> OMWPHandlerResult:
            from globals import request_info

            return OMWPHandlerResult200(request_info.path_info)

        self.environ['PATH_INFO'] = '/hello'

        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"/hello"])

    def test_headers(self) -> None:
        @self.omwp.route('/hello')
        def hello() -> OMWPHandlerResult:
            from globals import request_info
            if len(request_info.headers.items()) > 0:
                return OMWPHandlerResult200("Hello")
            else:
                return OMWPHandlerResult500()

        self.environ['PATH_INFO'] = '/hello'
        self.environ['HTTP_HOST'] = 'localhost:8080'

        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"Hello"])

    def test_http_method(self) -> None:
        @self.omwp.route('/hello')
        def hello() -> OMWPHandlerResult:
            from globals import request_info
            return OMWPHandlerResult200(str(request_info.http_method))

        self.environ['PATH_INFO'] = '/hello'
        self.environ['REQUEST_METHOD'] = 'POST'

        result = self.omwp(self.environ, self.start_response)
        self.assertEqual(result, [b"POST"])
