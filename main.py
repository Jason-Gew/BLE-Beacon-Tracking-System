# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import json
import time
# import paho.mqtt.client as mqtt
from configuration import AppConfig


datetime_format = "%Y-%m-%d %H:%M:%S %z"
config_file = 'config/app-config.ini'
app_config = None



def get_timestamp():
    ts = time.time()
    dtz = time.strftime(datetime_format, time.localtime(ts))
    return int(ts), dtz


def welcome():
    print("\n+---------------------------------------------------------------------+\n")
    print("+                  Bluetooth iBeacon Tracking Client                  +")
    print("\n+--------------------------- Version 2.0.0 ---------------------------+\n")
    time.sleep(0.5)


if __name__ == '__main__':
    welcome()
    ts, dt = get_timestamp()
    configure = AppConfig(config_file)
    configure.load()
    print("Client Initializing @ [{}] => AppConfig:\n{}".format(dt, configure))
    app_config = configure

