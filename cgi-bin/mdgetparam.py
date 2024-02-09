#!C:/Users/axis/anaconda3/python.exe

import os
import time
import requests
import re
import urllib.parse
import sys

# Get CGI command line arguments
args = dict(urllib.parse.parse_qsl(os.environ.get("QUERY_STRING")))

url = f"http://{args['cam_ip']}/axis-cgi/motion/mdgetparam.cgi"
s = requests.Session()
s.auth = (args['user'], args['password'])

print("Content-Type: application/json; charset=UTF-8\r\n\r\n")

with s.get(url,stream=True) as resp:	
	results = re.search(".*left=([0-9]+).*top=([0-9]+).*right=([0-9]+).*bottom=([0-9]+).*", str(resp.content))
	print(f"{{\"left\": {results.group(1)}, \"top\": {results.group(2)}, \"right\": {results.group(3)}, \"bottom\": {results.group(4)}}}\r\n\r\n", flush=True)
