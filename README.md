## BLE-Beacon-Tracking-System


<div style="text-align:right">
    <span style="float:right">
        By <a href="https://jason-gew.github.io" target="_blank"> Jason/GeW </a>&nbsp;
    </span>
</div>

<br/>
<br/>

Indoor Beacon Tracking system based on Bluetooth Low Energy and iBeacon technology. 
The tracking client can be installed on any Linux based micro-computer such as Raspberry Pi. 
~~It identifies each UUID of the beacons and utilizes Python multi-threading to record the entry time,
exit time, duration in the particular area with corresponding event~~. In the meanwhile, 
the client sends real-time event data to IoT cloud ~~by TCP~~. 
Further big data analytics and beacon visualization will be processed on cloud.

For indoor positioning and triangulation, multiple clients (hardware, at least 3+) 
should be placed in correct location according to reasonable coordination.


> Finally, it's the time to upgrade the system and move forward! (Coming in April 2021) 😎

### Upgrade Features
1. Replace old Python 2.7.x to Python 3.8.x in order to support more fancy Python functions and modules.


2. Integrate MQTT Pub/Sub capability. The tracking client will **publish** system and beacon events to IoT cloud via 
   [MQTT 3.1.1](https://github.com/mqtt/mqtt.org/wiki/Differences-between-3.1.0-and-3.1.1)
   or [MQTT 5.0](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html).
Besides, the client will subscribe to a command topic to receive service commands for real-time configuration updating 
   or further operations such as restart. All messages are in JSON format!
The topic structure:
```bash
 Event:   service/${region}/event/${client-uuid}
 Command: service/${region}/cmd/${client-uuid}
 Data:    service/${region}/data/${client-uuid}
```


3. Integrate sliding window algorithm to reduce the side effect of multi-path, 
   and send better average RSSI values for each supervised beacon.
   

4. Based on MQTT subscription, setup dynamic RSSI fence/threshold, for easy installation and debugging.


5. Add [SQLite3](https://docs.python.org/3/library/sqlite3.html) for better beacon UUID management on edge-devices.


6. Upgrade beacon tracking logic on client side.



### Installation
Some Linux libraries and Python packages are required:
```bash
sudo apt install libbluetooth-dev
sudo apt install libboost-python-dev
sudo apt install libboost-thread-dev
sudo pip3 install gattlib
sudo pip3 install pybluez
sudo pip3 install paho-mqtt
sudo pip3 install sqlalchemy
```
Or pip install based on _requirements.txt_

### MQTT Command Req and Resp Example
**Query Client Machine Status**
```json
{
   "command": "status",
   "trace": "test-trace-uid"
}
```
**Shutdown the Beacon Tracking Client**
```json
{
   "command": "shutdown",
   "trace": "test-trace-uid"
}
```
**Publish one-time beacon scan command** (duration is optional)
```json
{
   "command": "scan",
   "duration": 5, 
   "trace": "test-trace-uid"
}
```
Response
```json
{
  "data_type" : "JSONArray",
  "action" : "data",
  "message" : "OK",
  "timestamp" : "2021-04-04 23:50:03 +0800",
  "data" : [ {
    "uuid" : "06f62a6d-f66f-88bd-b66e-2b12fd6e96aa",
    "major" : 0,
    "minor" : 512,
    "power" : 171,
    "rssi" : -43,
    "address" : "34:D6:66:E7:34:88"
  }, {
    "uuid" : "06f6213d-f88e-aabc-a36d-2b49fd6c36ad",
    "major" : 0,
    "minor" : 0,
    "power" : 191,
    "rssi" : -47,
    "address" : "28:E4:C2:E6:A1:D2"
  } ]
}
```
**Change Scan Mode to Auto** (duration is optional)
```json
{
   "command": "change-scan-mode",
   "scan-mode": "auto",
   "duration": 3, 
   "trace": "test-trace-uid"
}
```


### Addition
Server side code based on Spring Boot 2.4.x and ReactJS framework,
old project has been moved to branch v2015-1-3

You are welcome to ask any questions [here](https://github.com/Jason-Gew/BLE-Beacon-Tracking-System/issues)!

