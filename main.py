# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import json
import time
# import paho.mqtt.client as mqtt
from configuration import AppConfig


DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
CONFIG_PATH = 'config/app-config.ini'
COMMAND_PATH = 'config/commands.json'
APP_CONFIG = None



def get_timestamp():
    ts = time.time()
    dtz = time.strftime(DATETIME_FORMAT, time.localtime(ts))
    return int(ts), dtz


def welcome():
    print("\n+---------------------------------------------------------------------+\n")
    print("+                  Bluetooth iBeacon Tracking Client                  +")
    print("\n+--------------------------- Version 2.0.0 ---------------------------+\n")
    time.sleep(0.5)


if __name__ == '__main__':
    welcome()
    ts, dt = get_timestamp()
    configure = AppConfig(CONFIG_PATH)
    configure.load()
    print("Client Initializing @ [{}] => AppConfig:\n{}".format(dt, configure))
    APP_CONFIG = configure

