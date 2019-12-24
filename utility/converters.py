#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import base64


def encode_url(url):
    return base64.urlsafe_b64encode(bytes(url, encoding='UTF-8')).decode('UTF-8')
    
def decode_url(uid):
    return base64.urlsafe_b64decode(uid).decode('UTF-8')
