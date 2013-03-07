import json
import serial
import string
from flask import Flask

if __name__ == "__main__":
    app = Flask(__name__)
    
    @app.route('/sensor/<sensor>')
    def sensor_handler(sensor):
        while True:
            ser = serial.Serial("/dev/ttyUSB0", 9600)
            s = ser.readline().strip()
            
            if s != '\x00':
                ar = s.split(':')
                if len(ar) == 3 and ar[1] == sensor:
                    return json.dumps({"sensor":sensor,"value":ar[2]})
   
    app.run(host='0.0.0.0',port=8111)
