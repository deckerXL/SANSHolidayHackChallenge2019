import re
import urllib.parse
import requests
import typing
import base64
import time

from mitmproxy import http
for i in range(30):
	response=requests.get('https://studentportal.elfu.org/validator.php')
	r = str(response.text)
	(r1,r2) = r.split('_')
	d1 = str(base64.b64decode(r1).decode("utf-8"))
	d2 = str(base64.b64decode(r2).decode("utf-8"))
	print (r + "\t" + d1 + "\t" + d2)
	time.sleep(1)
