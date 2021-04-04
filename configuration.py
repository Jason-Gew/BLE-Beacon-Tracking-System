#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

import configparser as cp
import json
import uuid
import re

CLIENT_SECTION = 'client'
MQTT_SECTION = 'mqtt'


class AppConfig(object):
    # App Default
    name = ''
    uuid = ''
    mac = ''
    # MQTT
    broker = ''
    port = 1883
    tls = False
    username = ''
    password = ''
    connection_timeout = 10
    keep_alive = 60,
    pub_qos = 1,
    sub_qos = 1,
    event_topic = ''
    cmd_topic = ''
    data_topic = ''

    def __init__(self, config_path):
        super().__init__()
        self.config = cp.RawConfigParser()
        self.config.read(config_path)

    def load(self):
        self.name = self.config.get(CLIENT_SECTION, 'name')
        self.mac = '-'.join(re.findall('..', '%012x' % uuid.getnode()))
        self.uuid = self.config.get(CLIENT_SECTION, 'uuid')
        if self.uuid is None or self.uuid == '':
            self.uuid = self.mac
        self.broker = self.config.get(MQTT_SECTION, 'broker')
        self.port = self.config.getint(MQTT_SECTION, 'port')
        self.tls = self.config.getboolean(MQTT_SECTION, 'tls')
        self.username = self.config.get(MQTT_SECTION, 'username')
        self.password = self.config.get(MQTT_SECTION, 'password')
        self.connection_timeout = self.config.getint(MQTT_SECTION, 'connectionTimeout')
        self.keep_alive = self.config.getint(MQTT_SECTION, 'keepAlive')
        self.pub_qos = self.config.getint(MQTT_SECTION, 'pubQos')
        self.sub_qos = self.config.getint(MQTT_SECTION, 'subQos')
        self.cmd_topic = self.config.get(MQTT_SECTION, 'cmdTopic')
        if self.cmd_topic.find('${mac}') != -1:
            self.cmd_topic = self.cmd_topic.replace('${mac}', self.mac)
        elif self.cmd_topic.find('${uuid}') != -1:
            self.cmd_topic = self.cmd_topic.replace('${uuid}', self.uuid)
        self.event_topic = self.config.get(MQTT_SECTION, 'eventTopic')
        if self.event_topic.find('${mac}') != -1:
            self.event_topic = self.event_topic.replace('${mac}', self.mac)
        elif self.event_topic.find('${uuid}') != -1:
            self.event_topic = self.event_topic.replace('${uuid}', self.uuid)
        self.data_topic = self.config.get(MQTT_SECTION, 'dataTopic')
        if self.data_topic.find('${mac}') != -1:
            self.data_topic = self.data_topic.replace('${mac}', self.mac)
        elif self.data_topic.find('${uuid}') != -1:
            self.data_topic = self.data_topic.replace('${uuid}', self.uuid)

    def __repr__(self):
        self.config = None
        variables = vars(self)
        del variables['config']
        return json.dumps(variables, skipkeys=False, indent=2)



