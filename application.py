#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bluetooth LE Beacon Tracking Client Main Entry

__author__ = 'Jason/GeW'
__version__ = '2.0.0'

import json
import time
import queue
import threading
import command_parser
import beacon_scanner
from app_logger import Logger
from mqtt_util import MqttUtil
from mqtt_util import MqttMsg
from configuration import AppConfig
from typing import Optional, Callable, Any, Iterable, Mapping


# -------- Static Variables Start --------
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %z"
CONFIG_PATH = 'config/app-config.ini'
COMMAND_PATH = 'config/commands.json'
COMMAND_KEY = 'command'
TRACE_KEY = 'trace'
APP_CONFIG = None
# -------- Static Variables End --------
log = Logger('logs/app.log').logger


def get_timestamp():
    ts = time.time()
    dtz = time.strftime(DATETIME_FORMAT, time.localtime(ts))
    return int(ts), dtz


def welcome():
    print("\n+---------------------------------------------------------------------+\n")
    print("+                 Bluetooth LE Beacon Tracking Client                 +")
    print("\n+--------------------------- Version {} ---------------------------+\n".format(__version__))
    time.sleep(0.5)


class CommandListener(threading.Thread):
    """
    CommandListener for cmd process from MQTT Subscription
    """
    msg_queue = None
    mqtt_client = None
    stop = False

    def __init__(self, thread_name, msg_queue, mqtt_client) -> None:
        self.msg_queue = msg_queue
        if mqtt_client is None or not isinstance(mqtt_client, MqttUtil):
            raise TypeError("Invalid MqttUtil")
        else:
            self.mqtt_client = mqtt_client
        threading.Thread.__init__(self, name=thread_name)

    def run(self) -> None:
        while not self.stop:
            if not self.msg_queue.empty():
                message = None
                try:
                    msg = dict(self.msg_queue.get())
                    message = msg.get('message')
                    cmd_dict = json.loads(message)
                    if COMMAND_KEY in cmd_dict.keys():
                        cmd = cmd_dict.get(COMMAND_KEY)
                        if 'status' == cmd:
                            system_status = json.dumps(command_parser.show_system_status())
                            self.mqtt_client.publish(system_status)
                            log.info("Published System Status: " + system_status)
                        elif 'shutdown' == cmd:
                            log.info("Received Shutdown Command: " + message)
                            if cmd_dict.get(TRACE_KEY) is None or len(str(cmd_dict.get(TRACE_KEY))) <= 3:
                                log.warning("Shutdown Command Does Not Have Valid Trace")
                                continue
                            self.stop = True
                            client_message = MqttMsg('String', cmd, 'System Will Shutdown After 3 Seconds',
                                                     cmd_dict.get(TRACE_KEY))
                            self.mqtt_client.publish(client_message.to_json())
                            time.sleep(3)
                            self.mqtt_client.disconnect()
                            exit(0)
                        elif ('beacon-scan' == cmd or 'scan' == cmd) and cmd_dict.get(TRACE_KEY) is not None:
                            scan_duration = cmd_dict.get('duration')
                            beacon_data = []
                            log.info("Received Manual Beacon-Scan Requirement, Duration={}".format(scan_duration))
                            if scan_duration is not None and 1 <= scan_duration < 10:
                                beacon_data = beacon_scanner.scan(scan_duration)
                            else:
                                beacon_data = beacon_scanner.scan()
                            client_message = MqttMsg('JSONArray', cmd, 'OK', data=list(beacon_data))
                            self.mqtt_client.publish(client_message.to_json(), APP_CONFIG.data_topic)
                        else:
                            log.info("Unknown Command: " + message)

                except json.decoder.JSONDecodeError as te:
                    log.error("Invalid JSON Command Type for Msg={} : {}".format(message, te))
                except RuntimeError as re:
                    log.error('Process Command Msg Failed: {}'.format(re))
            time.sleep(0.5)

    def join(self, timeout: Optional[float] = ...) -> None:
        self.stop = True
        super(CommandListener, self).join()


if __name__ == '__main__':
    welcome()
    ts, dt = get_timestamp()
    configure = AppConfig(CONFIG_PATH)
    configure.load()
    log.info("Beacon Tracking Client Initializing @ [{}] => AppConfig:\n{}".format(dt, configure))
    APP_CONFIG = configure
    queue = queue.Queue(1024)
    MQTT_UTIL = MqttUtil(configure, queue)
    MQTT_UTIL.connect()
    MQTT_UTIL.subscribe()
    cmdListener = CommandListener('Command-Listener', queue, MQTT_UTIL)
    try:
        cmdListener.start()
        MQTT_UTIL.client.loop_forever()
    except KeyboardInterrupt as ki:
        log.info("User Terminate the Client...\n\n====== Thank You for Using BLE Beacon Tracking Client V{} ======\n\n"
                 .format(__version__))
        cmdListener.join()
        MQTT_UTIL.disconnect()
        exit(0)

