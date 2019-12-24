#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

from bs4 import BeautifulSoup

sys.path.append('/home/jeremy/Library/')

from document.text_document import read_document



    
def headline(node, c):
    return next((l.text for l in node.formatted_text if l.tag == 'h1'), None)
    
def subhead(node, c):
    return next((l.text for l in node.formatted_text if l.tag == 'h2'), None)


