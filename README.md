# AXIS 2420 Motion Detect WebPage and D4100-E Demo Instructions

This document outlines how to install and run the 2420 WebPage and D4100-E demo.
It is based on Apache 2.4 running on a Windows server (an AXIS S1148 was used for the development), Python3 is used for CGI scripts,
an AXIS 2420 Network camera is used for motion detection and an AXIS D4100-E strobe for visual indication of alarm status.

The Dropbox folder contains a few different files depending on how the reader prefers to install the system:

# httpd-2.4.58, this is a Vanilla Apache24 dist for Win64 if the reader prefers to start with a clean install
# Complete_Apache_Install, This is a compressed folder containing all Apache config, html and cgi scripts needed to run the integration
# Anaconda - Anaconda python installation file.
# 2420_demo_cgi_html, This is a collection of just the cgi-bin, htdocs and conf folders of Apache that you could add into a Vanilla Apache24 installation

# Demo Summary
The demo does the following:

Webpage visualization of Motion Detection status, polls the motiondetect-cgi of the AXIS 2420 (using JavaScript Streams API)
Visualizes the current motion window in green if there is no motion, red for 5 seconds after motion
If motion is triggered and more than 5 seconds has passed since last strobe fire, trigger the strobe to flash for 10 seconds
Some caveats / disclaimers
Apache was used over other lightweght server options since it does not buffer cgi output, since the motiondetect cgi is a continuous stream,
other web servers would never flush data out for the browser to handle the events
ACS likes to keep the web code running even though you close the webpage, doesn’t close until entire client is closed
Above is good to know as the 2420 seems to struggle / stop sending motion data if too many clients connect
I added a restart command button in ACS for any case where the 2420 locks up.
For now this implementation does not provide config of the motion Window. I recommend installing IE Tabs, IE Tabs Helper, Java (and add security exception for camera IP)
for the motion window config.
Also for now this demo only works for one motion window.
Installation Instructions

# Here is a summary of what needs to be done

Install Python3
Install and Configure Apache24
Make sure HTML and cgi files are copied into the correct folders on Apache directory
Change Python script she-bangs to correct Windows path for Python
Provide IP address and credentials for 2420 and D4100-E
Configure strobe event
Run Apache Server
Connect via browser
Install Python3
Download and execute the Anaconda Python installer. I recommend adding Python to the system PATH at least if this is being run on e.g. a dedicated ACS server.
Take note of the installation path, on my S1148 server

C:/Users/axis/anaconda3/python.exe
This is needed later when modifying the Python scripts.

Install Apache
Installing Apache is simple. Simply unpack the directory (either w/ project config or vanilla) directly on your C-drive.
With the config files provided, that path to the Apache binary should then be:

C:\>Apache24\Apache24\bin\httpd.exe
If the reader started with a vanilla Apache instead of the pre-packaged, There are some configuration changes needed in the Apached conf file:
(if using the pre-packaged, just skip below unless there are issues)

C:\>Apache24\Apache24\conf\httpd.conf
First, make sure SRVROOT is correct at the beginning of the conf file,
should look like this:

#
# ServerRoot: The top of the directory tree under which the server's
# configuration, error, and log files are kept.
#
# Do not add a slash at the end of the directory path.  If you point
# ServerRoot at a non-local disk, be sure to specify a local disk on the
# Mutex directive, if file-based mutexes are used.  If you wish to share the
# same ServerRoot for multiple httpd daemons, you will need to change at
# least PidFile.
#
Define SRVROOT "c:/Apache24/Apache24"
Second, make sure Apache will execute Python scripts as CGI:
Find and modify the below accordingly

#
    # AddHandler allows you to map certain file extensions to "handlers":
    # actions unrelated to filetype. These can be either built into the server
    # or added with the Action directive (see below)
    #
    # To use CGI scripts outside of ScriptAliased directories:
    # (You will also need to add "ExecCGI" to the "Options" directive.)
    #
    AddHandler cgi-script .cgi .py .bat
I also allowed CGI execution in non-standard folders:

#
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"
    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks ExecCGI
Copy files
Make sure the contents of cgi-bin, htdocs are copied in to the Apache directory.
This is already packaged in the “Complete_Apache” zip file but if the reader started with Vanilla Apache, these need to be copied over.

Change Python Scripts
The reader needs to modify the first line of each Python script to include the correct full path of Python3 on their system
Modify the three CGI-scripts, motiondetect.py, vinput.py, and mdgetparams.py accordingly

Below is an example where Python is installed under:

motiondetect.py

#!C:/Users/axis/anaconda3/python.exe
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
            
Configure IP addresses
Edit htdocs/devices.conf according to your network setup, see below an example.
This is standard JSON format and should be fairly self-explanatory. The CGI communicate over HTTP with the devices, basic auth for the 2420 and Digest for the D4100-E.
Make sure HTTP is not disabled on the D4100-E (ACS sets HTTPS only)

{"cam_ip": "192.168.2.192", 
 "cam_user": "root",
 "cam_password": "pass",
 "strobe_ip": "192.168.3.178",
 "strobe_user": "root",
 "strobe_password": "pass"}
###Configure strobe event

Configure a light profile and event on the D4100-E strobe to flash a light for 10 seconds when VirtualInput 64 is activated.
The vinput.py CGI will enable vinput 64 for 5 seconds on each motion detect

Run Apache
After this configuration has been done, start Apache from a terminal:

C:\>Apache24\Apache24\bin\httpd.exe
If you want Apache to start as a service, follow the instructions on the Apache website to do this. Or just create a .bat file with the above command.

Connect via browser
Now it should be possible to load the webpage via a browser, for example if on the local machine:

http://localhost
ACS Restart command
Here is the HTTP Post command to use for an action button in ACS to restart the 2420:

URL: http://192.168.2.192/this_server/ServerManager.srv

Data: do_reboot=yes&do_factory_default=no&servermanager_return_page=%2Fadmin%2Fsup_restart.shtml&servermanager_do=set_variables
