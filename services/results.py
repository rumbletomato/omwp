from typing import Optional


class OMWPHandlerResult:
    def __init__(self, status: str, payload: str = "") -> None:
        self._status: str = status
        self._payload: str = payload

    @property
    def payload(self) -> Optional[bytes]:
        return self._payload.encode()

    @property
    def status(self) -> str:
        return self._status


class OMWPHandlerResult404(OMWPHandlerResult):
    def __init__(self) -> None:
        super().__init__("404 Not Found", "I couldn't find it..")


class OMWPHandlerResult200(OMWPHandlerResult):
    def __init__(self, payload: str = "") -> None:
        super().__init__("200 Ok", payload)


class OMWPHandlerResult500(OMWPHandlerResult):
    def __init__(self) -> None:
        super().__init__("500 Internal Server Error", "Ooops! Something went wrong...")
