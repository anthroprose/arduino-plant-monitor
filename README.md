arduino-plant-monitor
=====================

## v1.0.0 - 03/07/2013

### Info
Use an Arduino+Seeduino components to monitor the moisture level of soil so we can tell when the plants need watering.

Currently monitors two plants, with built in thresholding.

Ability to launch a REST interface for polling the sensors as well as a PUSH notification system for sending Zenoss Events with the JSON API.

### References

 * http://imgur.com/Jymhmue
 * http://seeedstudio.com/wiki/Grove_-_Moisture_Sensor
 
### Config
```json
host : "my.zenoss.com",
user : "admin",
passwd : "pass",
usb : "/dev/ttyUSB0",
proto : "https"
```