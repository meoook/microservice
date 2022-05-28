from typing import Literal

from requests import Session, RequestException
from requests.packages import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.singleton import Singleton

urllib3.disable_warnings(InsecureRequestWarning)

HttpMethod = Literal['GET', 'POST', 'PUT', 'DELETE']


class AppSessionException(Exception):
    def __init__(self, message):
        super().__init__(f'[http] {message}')


class AppSession(Singleton):
    def __init__(self):
        self.__headers = {}
        self.__session = Session()

    def request(self, url: str, method: HttpMethod = 'GET', headers: dict[str, str] = None, **kwargs) -> any:
        assert url, AppSessionException(f'url not set to make request')
        _headers = headers if headers else self.__headers

        try:
            _response = self.__session.request(method=method, url=url, headers=_headers, timeout=10, **kwargs)
        except RequestException as _err:
            raise AppSessionException(f'{method} to {url} failed - {_err}')

        if _response.status_code < 300:
            return _response.json()
        raise AppSessionException(f'{method} to {url} failed with code {_response.status_code}')

    def get(self, url: str, headers: dict[str, str] = None, params: dict[str, str] = None, **kwargs):
        return self.request(url=url, method='GET', headers=headers, params=params, **kwargs)

    def post(self, url: str, headers: dict[str, str] = None, json: dict = None, **kwargs):
        return self.request(url=url, method='POST', headers=headers, json=json, **kwargs)
