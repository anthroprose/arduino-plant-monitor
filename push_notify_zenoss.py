# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python testdaemon.py start
#logger.debug("Debug message")
#logger.info("Info message")
#logger.warn("Warning message")
#logger.error("Error message")
            
#standard python libs
import logging
import time
import pprint
import datetime
import sys
import os
import json
import urllib2
import base64
import httplib2 as http
import serial

#third party libs
from daemon import runner
from datetime import datetime
from os import environ

class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/plant_monitor.pid'
        self.pidfile_timeout = 5
        self.success = True

        
    def run(self):
        
        try:
            while True:
                
                ser = serial.Serial("/dev/ttyUSB0", 9600)
                s = ser.readline().strip()
            
                if s != '\x00':
                    ar = s.split(':')
                    if len(ar) == 3:
                        
                        ar[2] = int(ar[2])
                        
                        if ar[2] >= 900:
                            self.sendevent(ar[1], 'Plant recently watered - ' + str(ar[2]), 'Moisture', 'Clear')
                        elif ar[2] >= 600:
                            self.sendevent(ar[1], 'Moisture reading is good - ' + str(ar[2]), 'Moisture', 'Info')
                        elif ar[2] >= 400:
                            self.sendevent(ar[1], 'Moisture reading is becoming too low - ' + str(ar[2]), 'Moisture', 'Warning')
                        elif ar[2] >= 200:
                             self.sendevent(ar[1], 'Moisture reading is becoming dangerously low - ' + str(ar[2]), 'Moisture', 'Error')
                        elif ar[2] >= 0:
                             self.sendevent(ar[1], 'Moisture reading is dangerously low - ' + str(ar[2]), 'Moisture', 'Critical')
                        else:
                            pprint.pprint('fallthough')
                
                        time.sleep(300)
                
        except:
            self.success = False
            self.log('Global', 'instance', "Uncaught Exception: " + str(sys.exc_info()), 'error')


    def sendevent(self, sensor, msg, component, severity):
        
        try:
            from urlparse import urlparse
        except ImportError:
            from urllib.parse import urlparse

        headers = {
                   'Accept': 'application/json',
                   'Content-Type': 'application/json; charset=UTF-8',
                   'Authorization': "Basic {0}".format(base64.b64encode(self.user + ":" + self.passwd)),
        }

        path = '/zport/dmd/evconsole_router'
        target = urlparse(self.endpoint+path)
        method = 'POST'
        
        body = '{"action":"EventsRouter","method":"add_event","data":[{"device":"' + str(sensor) + '", "summary":"' + str(msg) + '", "component":"' + str(component) + '", "severity":"' + str(severity) + '", "evclass":"/Arduino/Sensors/Plants", "evclasskey":"" }],"tid":1}'
        
        h = http.Http(disable_ssl_certificate_validation=True)
        response, content = h.request(target.geturl(), method, body, headers)
        data = json.loads(content)
            

    def log(self, guid, action, msg, level = 'event'):
        pprint.pprint(action + ': ' + msg)
        if level == 'event':
            logger.info(action + ': ' + msg)
        elif level == 'error':
            logger.error(action + ': ' + msg)

app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/plant_monitor.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()