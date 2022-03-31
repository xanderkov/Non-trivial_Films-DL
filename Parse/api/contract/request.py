from __future__ import annotations
from abc import ABC
from typing import Dict
from urllib.parse import urlencode

from kinopoisk_unofficial.client.http_method import HttpMethod
from kinopoisk_unofficial.contract.response import Response


class Request(ABC):
    METHOD: HttpMethod = HttpMethod.GET
    PATH: str = '/'
    RESPONSE: type = Response

    def method(self) -> HttpMethod:
        return self.METHOD

    def path(self) -> str:
        return self.PATH

    def response_class(self) -> type:
        return self.RESPONSE

    @staticmethod
    def _build_url(url: str, params: Dict) -> str:
        return url + '?' + urlencode(params)
