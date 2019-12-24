#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  project_status.py
#  
import sys
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


import logging
logger = logging.getLogger(__name__)
env = Environment(loader=FileSystemLoader('/home/jeremy/Templates'))


def write_html_document(filepath, template, **content):
    try:
        template = env.get_template(template)
    except FileNotFoundError:
        raise FileNotFoundError
        
    try:
        text = template.render(**content)
    except Exception as e:
        print(e)
        return False
    
    try:
        Path(filepath).write_text()
    except FileNotFoundError:
        raise FileNotFoundError
    return output_filepath
        

