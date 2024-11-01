import socket
import re
import requests
from http.client import HTTPConnection
from logger import log


class Endpoint:
    def __init__(self, url: str, cookies: str = None) -> None:
        self._url = url.strip().replace(' ', '')
        self._cookies = cookies

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        self._url = url

    @property
    def cookies(self) -> str:
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: str) -> None:
        self._cookies = cookies

    def getDomain(self) -> str:
        return self._url.split('/')[2]

    def getMainUrl(self) -> str:
        return '/'.join(self._url.split('/')[:3])

    def getPath(self) -> str:
        return '/'.join(self._url.split('/')[3:])

    def getSchema(self) -> str:
        return self._url.split(':')[0]

    def getIP(self) -> str:
        try:
            return socket.gethostbyname(self.getDomain())
        except:
            raise('Method getIP Error')

    def getCname(self) -> str:
        try:
            return socket.gethostbyaddr(self.getDomain())[0]
        except:
            raise('Method getCname Error')

    def checkUrl(self) -> str:
            return True
        

    def makeRequest(self, url: str = None, method: str = 'GET', headers: dict = None, timeout: int = None, protocolVersion: str = 'HTTP/1.1') -> bool:
        try:
            HTTPConnection._http_vsn_str = protocolVersion
            checkUrl = url if url else self._url
            status = requests.request(
                method=method, url=checkUrl, cookies=self._cookies, headers=headers, timeout=timeout).status_code
            if status != 403 and status != 401:
                log.info(f'[+] The request {method} {checkUrl} with Headers {headers} generated status code {status}')
            return True
        except:
            log.warning(f'[-] Exception generated by request {method} {checkUrl} with Headers {headers}')
            return False

    def __str__(self) -> str:
        return f'Endpoint with url:{self._url} and cookies:{self._cookies}'
