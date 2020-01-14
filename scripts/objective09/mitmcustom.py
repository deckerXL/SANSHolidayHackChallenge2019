import re
import urllib.parse
import requests
import typing

from mitmproxy import http

# set of SSL/TLS capable hosts
secure_hosts: typing.Set[str] = set()

def request(flow: http.HTTPFlow) -> None:
    response=requests.get('https://studentportal.elfu.org/validator.php')
    response_bytes = response.text.encode()
    flow.request.content = flow.request.content.replace(b'token=REPLACE', b'token='+response_bytes)
