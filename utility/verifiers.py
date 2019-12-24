#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

def filter_by_key_value(item, key, *values):
    try:
        return item[key] in values
    except KeyError as e:
        print(f' no {e} in {item}')
    return False
