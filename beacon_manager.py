#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean


Base = declarative_base


class BeaconInfo(Base):
    __tablename__ = 'ble_beacon_info'
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    create_time = Column("create_time", DateTime, default=datetime.now)
    update_time = Column("update_time", DateTime, nullable=True)
    address = Column("address", String, nullable=False, unique=True)
    uuid = Column("uuid", String, nullable=False, unique=True)
    active = Column("active", Boolean, nullable=False)
    extra_info = Column("extra_info", String, nullable=True)

    def __init__(self):
        pass

    def __repr__(self):
        return "id={}, create_time={}, update_time={}, address={}, uuid={}, " \
               "active={}, extra_info={}".format(self.id, self.create_time, self.update_time, self.address, self.uuid,
                                                 self.active, self.extra_info)

