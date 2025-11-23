# pylint: disable=invalid-name,line-too-long,missing-function-docstring

import json
import ssl
import urllib
import urllib.error
from typing import Union
from urllib import request
from http.client import HTTPResponse

ALVERSION = "v1.9.0.0"


class AstroRequests():
    @classmethod
    def _setup_context(cls) -> tuple[ssl.SSLContext, request.OpenerDirector]:
        """Set up SSL context and proxy handler for requests."""
        proxies = request.getproxies()
        proxy_handler = request.ProxyHandler(proxies)
        opener = request.build_opener(proxy_handler)
        gcontext = ssl._create_unverified_context()
        request.install_opener(opener)
        return gcontext, opener

    @classmethod
    def get(cls, url: str, timeout: int = 5) -> Union[HTTPResponse, urllib.error.HTTPError]:
        """Send GET request to specified URL."""
        gcontext, _ = cls._setup_context()
        try:
            resp = request.urlopen(url, timeout=timeout, context=gcontext)
        except urllib.error.HTTPError as e:
            resp = e
        return resp

    @classmethod
    def post(cls, url: str, headers: dict | None = None, jsonD: dict | None = None, timeout: int = 5) -> Union[HTTPResponse, urllib.error.HTTPError]:
        """Send POST request to specified URL with optional JSON data."""
        if headers is None:
            headers = {}
        if jsonD is None:
            jsonD = {}

        req = request.Request(url)
        data = None
        if jsonD:
            data = json.dumps(jsonD).encode('utf-8')
            req.add_header('Content-Type', 'application/json; charset=utf-8')

        for header, value in headers.items():
            req.add_header(header, value)

        gcontext, _ = cls._setup_context()
        try:
            resp = request.urlopen(
                req, data=data, timeout=timeout, context=gcontext)
        except urllib.error.HTTPError as e:
            resp = e
        return resp
