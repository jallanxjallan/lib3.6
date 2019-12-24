#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

from collections import namedtuple

from utility.helpers import title_case




MI = namedtuple('MenuItem', ('href, label'))

def children(node, c):
    return [MI(c.name, title_case(c.name))  for c in node.children]

def siblings(node, c):
    return [MI(s.name, title_case(s.name))  for s in node.siblings]
