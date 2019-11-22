from enum import Enum


class HttpMethod(Enum):
    GET = 'GET'
    HEAD = 'HEAD'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    CONNECT = 'CONNECT'
    OPTIONS = 'OPTIONS'
    TRACE = 'TRACE'
    PATCH = 'PATCH'

    def __str__(self):
        return self.value


class RequestInfo:
    def __init__(self) -> None:
        self.path_info: str = ""
        self.http_method: HttpMethod = HttpMethod.GET
        self.headers: dict = {}


request_info: RequestInfo = RequestInfo()
