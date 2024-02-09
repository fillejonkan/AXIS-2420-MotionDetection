#!C:/Users/axis/anaconda3/python.exe

import os
import time
import requests
from requests.auth import HTTPDigestAuth
import urllib.parse
import sys

args = dict(urllib.parse.parse_qsl(os.environ.get("QUERY_STRING")))
#args = dict(urllib.parse.parse_qsl(sys.argv[1]))

print("Content-Type: text/plain; charset=UTF-8\r\n\r\n")

s      = requests.Session()
s.auth = HTTPDigestAuth(args['user'], args['password'])

resp =  s.get(f"http://{args['ip']}/axis-cgi/virtualinput/deactivate.cgi?port=64&schemaversion=1")
resp = s.get(f"http://{args['ip']}/axis-cgi/virtualinput/activate.cgi?port=64&schemaversion=1")
time.sleep(5)
resp =  s.get(f"http://{args['ip']}/axis-cgi/virtualinput/deactivate.cgi?port=64&schemaversion=1")

print("\r\n\r\n", flush=True)