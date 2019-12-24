#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

import logging
from redis_log_handler import RedisKeyHandler

def get_redis_logger(key):
    handler = RedisKeyHandler(key)  # Default parameters for Redis connection are used
    logger = logging.getLogger()  # No name gives you the root logger
    logger.setLevel("INFO")
    logger.addHandler(handler)
    return logger
