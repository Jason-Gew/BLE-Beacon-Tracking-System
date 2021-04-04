#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import json
import time
import psutil
import platform


SYSTEM_CMD = []
APP_CMD = []
INIT = False
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"


class BaseCommand(object):
    key = ''
    type = ''
    request_type = ''
    response_type = ''

    def __init__(self) -> None:
        super().__init__()
        pass


def load_commands(path):
    global SYSTEM_CMD, APP_CMD
    with open(path, 'r') as cmd_file:
        cmd = json.load(cmd_file)
        SYSTEM_CMD = dict(cmd).get('system')
        APP_CMD = dict(cmd).get('app')


def show_system_status():
    status_info = {'os': platform.uname().system,
                   'core': psutil.cpu_count(),
                   'processor': platform.uname().processor,
                   'cpuUsage': psutil.cpu_percent(),
                   'hostname': platform.uname().node,       # For Secure Purpose, May Need to Remove
                   'memoryUnit': "MB",
                   'totalMemory':  int(psutil.virtual_memory().total / (1024 * 1024)),
                   'usedMemory': int(psutil.virtual_memory().used / (1024 * 1024)),
                   'memoryUsage': psutil.virtual_memory().percent,
                   'usageUnit': "%",
                   'offsetDateTime': time.strftime(DATETIME_FORMAT, time.localtime(time.time()))}
    network_info = {}
    addresses = psutil.net_if_addrs()
    for interface_name, interface_addresses in addresses.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                network_info[interface_name] = address.address
    status_info.update(network_info)
    return status_info


# Test Only
if __name__ == '__main__':
    load_commands('config/commands.json')
    print(show_system_status())

