# -*- coding: utf-8 -*-
__author__ = 'Jason/GeW'
import os
import logging
from logging import handlers


# App Standard Logger
class Logger(object):
    levels = {
        'debug': logging.DEBUG,
        'Debug': logging.DEBUG,
        'DEBUG': logging.DEBUG,

        'info': logging.INFO,
        'Info': logging.INFO,
        'INFO': logging.INFO,

        'warning': logging.WARNING,
        'Warning': logging.WARNING,
        'WARNING': logging.WARNING,

        'error': logging.ERROR,
        'Error': logging.ERROR,
        'ERROR': logging.ERROR,

        'critical': logging.CRITICAL,
        'Critical': logging.CRITICAL,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, filename, level='INFO', when='D', back_count=5,
                 formatter='%(asctime)s [%(levelname)s] - %(filename)s: %(message)s'):
        f_dir, f_name = os.path.split(filename)
        os.makedirs(f_dir, exist_ok=True)
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(formatter)
        self.logger.setLevel(self.levels.get(level))
        sh = logging.StreamHandler()  # Also Print to Screen
        sh.setFormatter(format_str)
        self.logger.addHandler(sh)
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when,
                                               backupCount=3 if back_count < 1 else back_count,
                                               encoding='utf-8')
        th.setFormatter(format_str)
        self.logger.addHandler(th)
