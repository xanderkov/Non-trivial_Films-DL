from kinopoisk_unofficial.client.http_method import HttpMethod
from kinopoisk_unofficial.contract.request import Request
from kinopoisk_unofficial.response.films.distributions_response import DistributionsResponse


class DistributionsRequest(Request):
    METHOD: HttpMethod = HttpMethod.GET
    PATH: str = '/api/v2.2/films/{id}/distributions'
    RESPONSE: type = DistributionsResponse

    __id: int

    def __init__(self, film_id: int) -> None:
        self.__id = film_id

    @property
    def id(self) -> int:
        return self.__id

    def path(self) -> str:
        return self.PATH.replace('{id}', str(self.id))
