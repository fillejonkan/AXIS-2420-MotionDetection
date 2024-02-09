#!C:/Users/axis/anaconda3/python.exe

import time
import requests
import re
import urllib.parse
import sys
import os


args = dict(urllib.parse.parse_qsl(os.environ.get("QUERY_STRING")))
#args = dict(urllib.parse.parse_qsl(sys.argv[1]))

url = f"http://{args['cam_ip']}/axis-cgi/motion/motiondetect.cgi"
s = requests.Session()
s.auth = (args['user'], args['password'])

print("Content-Type: text/event-stream; charset=UTF-8\r\n\r\n")

with s.get(url,stream=True) as resp:
    for line in resp.iter_lines(chunk_size=1):
        results = re.search("key=([0-9]+);level=([0-9]+);threshold=([0-9]+);", str(line))
        if results:
            print("event: motiondata")
            print(f"data: {{\"key\": {results.group(1)}, \"level\": {results.group(2)}, \"threshold\": {results.group(3)}}}\r\n\r\n", flush=True)