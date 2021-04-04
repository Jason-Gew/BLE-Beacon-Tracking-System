#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import os
import sys
import json
from bluetooth.ble import BeaconService


class BasicBeaconInfo(object):
    """
    Basic Beacon Info Data Model
    """
    def __init__(self, data_list, mac):
        self.uuid = data_list[0]
        self.major = data_list[1]
        self.minor = data_list[2]
        self.power = data_list[3]
        self.rssi = data_list[4]
        self.address = mac

    def to_dict(self):
        return vars(self)

    def to_json(self):
        return json.dumps(vars(self))


if 'linux' in sys.platform:
    os.system('sudo hciconfig hci0 up')
service = BeaconService()


def scan(duration=3):
    if duration < 1 or duration > 10:
        duration = 3
    beacon_info = []
    beacons = service.scan(duration)
    if beacons.items is None:
        return beacon_info
    for address, data in list(beacons.items()):
        if data is None:
            continue
        info = BasicBeaconInfo(data, address)
        beacon_info.append(info.to_dict())
    return list(beacon_info)


# Test Only
if __name__ == '__main__':
    results = scan()
    print(json.dumps(results, indent=2))

