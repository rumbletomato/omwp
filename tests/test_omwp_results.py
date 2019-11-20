from unittest import TestCase

from services.results import OMWPHandlerResult404, OMWPHandlerResult200


class OMWPHandlerResultsTest(TestCase):
    def test_result_404(self):
        result_404 = OMWPHandlerResult404()
        self.assertEqual(result_404.status, "404 Not Found")

    def test_result_200(self):
        result_200 = OMWPHandlerResult200()
        self.assertEqual(result_200.status, "200 Ok")
        self.assertEqual(result_200.payload, b"")

    def test_result_200_with_payload(self):
        payload = "Some useful payload"
        result = OMWPHandlerResult200(payload)
        self.assertEqual(result.payload, payload.encode())

    def test_invariant_result_status(self):
        result = OMWPHandlerResult404()
        with self.assertRaises(AttributeError):
            result.status = "200 Ok"

    def test_invariant_result_payload(self):
        initial_payload = "Some information"
        result = OMWPHandlerResult200(initial_payload)
        with self.assertRaises(AttributeError):
            result.payload = "Nothing"
