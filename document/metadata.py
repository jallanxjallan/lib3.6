#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr
from ruamel.yaml import YAML

import logging
logger = logging.getLogger(__name__)

yaml = YAML()
yaml.explicit_start = True
yaml.explicit_end = True

@attr.s
class DocMeta():
    pass
