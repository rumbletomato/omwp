from collections.abc import Callable
from unittest import TestCase

from services.handlers import OMWPHandler404
from services.results import OMWPHandlerResult404


class OMWPHandlersTest(TestCase):
    def test_handler_404(self):
        handler_404 = OMWPHandler404()
        self.assertIsInstance(handler_404, Callable)

        handler_result = handler_404()
        self.assertIsInstance(handler_result, OMWPHandlerResult404)
