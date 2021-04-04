#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import json
import time
import queue
import paho.mqtt.client as mqtt
from configuration import AppConfig
from app_logger import Logger


# MQTT Reason Code
reason_codes = {
    0: "Connection Successful",
    1: 'Connection Refused - Incorrect Protocol Version',
    2: 'Connection Refused - Invalid Client Identifier',
    3: 'Connection refused - Server Unavailable',
    4: 'Connection Refused - Bad Username or Password',
    5: 'Connection Refused - Not Authorised',
}


def get_timestamp():
    datetime_format = "%Y-%m-%d %H:%M:%S %z"
    ts = time.time()
    dtz = time.strftime(datetime_format, time.localtime(ts))
    return dtz


log = Logger('logs/mqtt.log').logger


class MqttUtil(object):
    """
    MQTT Simple Utility Client
    Messages from subscribed topic(s) will be delivered via queue
    """
    config = None
    msg_queue = None
    client = None
    init = False

    def __init__(self, app_config, msg_queue=None) -> None:

        if msg_queue is not None and isinstance(msg_queue, queue.Queue):
            self.msg_queue = msg_queue
        if not isinstance(app_config, AppConfig):
            raise TypeError("Invalid App Config")
        else:
            self.config = app_config
            self.client = mqtt.Client(self.config.uuid)
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_msg
            self.client.on_disconnect = self.on_disconnect
            self.client.enable_logger(log)

    def connect(self):
        self.init = True
        log.info("Connecting to MQTT Broker {}:{}".format(self.config.broker, self.config.port))
        result = self.client.connect(self.config.broker, self.config.port)
        return result

    def disconnect(self):
        if self.client is not None and self.client.is_connected():
            self.client.disconnect()
            log.info("Disconnected with Broker {}:{}".format(self.config.broker, self.config.port))

    def publish(self, message, topic=None, qos=0):
        if topic is None or topic == '':
            topic = self.config.event_topic
        if qos is None or qos == 0 or qos < 1 or qos > 2:
            qos = self.config.pub_qos
        if not self.init:
            self.connect()
        elif not self.client.is_connected():
            self.client.reconnect()
        try:
            if isinstance(message, MqttMsg):
                self.client.publish(topic, message.to_json(), qos)
            else:
                self.client.publish(topic, message, qos)
        except RuntimeError as re:
            log.error('Publish Message [{}] Failed: {}'.format(message, re))

    def subscribe(self, topic=None, qos=0):
        if topic is None or len(topic) < 3:
            topic = self.config.cmd_topic
        if qos is None or qos == 0 or qos < 1 or qos > 2:
            qos = self.config.sub_qos
        if not self.init:
            self.connect()
        elif not self.client.is_connected():
            self.client.reconnect()
        self.client.subscribe(topic, qos)
        log.info("MQTT Client Subscribe to Topic={} with qos={}".format(topic, qos))

    def unsubscribe(self, topic):
        if topic is None or self.client is None:
            pass
        else:
            self.client.unsubscribe(topic)
            log.info("MQTT Client Unsubscribe to Topic={}".format(topic))

    def on_msg(self, client, userdata, message):
        log.info("Received Message From Topic [{}]: \n{}".format(message.topic, message.payload.decode('utf-8')))
        if self.msg_queue is not None:
            combo = {'topic': message.topic, 'message': message.payload.decode('utf-8')}
            self.msg_queue.put(combo)
            log.info("Add Message to the Queue, Current Queue Capacity: {}".format(self.msg_queue.qsize()))

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected with Broker")
        else:
            log.error("Connect with Broker Failed! Code={} Reason={}".format(rc, reason_codes.get(rc)))

    @staticmethod
    def on_disconnect(client, userdata, rc):
        if rc == 0:
            log.info("Disconnected with Broker")
        else:
            log.error("Disconnect with Broker Code={} Reason={}".format(rc, reason_codes.get(rc)))


class MqttMsg(object):
    """
    Standard MQTT Message in JSON format
    """
    timestamp = None
    action = None
    data_type = ''
    data = None
    message = None

    def __init__(self, data_type, action, message, data=None) -> None:
        self.data_type = data_type
        self.action = action
        self.message = message
        self.timestamp = get_timestamp()
        self.data = data

    def to_json(self):
        return json.dumps(vars(self))


# Test Only
# if __name__ == '__main__':
#     configure = AppConfig('config/app-config.ini')
#     configure.load()
#     mqtt_client = MqttUtil(configure)
#     msg = MqttMsg(configure.uuid, "TEST", "Hello")
#     print(msg.to_json())
#     mqtt_client.connect()
#     mqtt_client.publish(msg)
#     mqtt_client.subscribe()
#     mqtt_client.client.loop_forever()
