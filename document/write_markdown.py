#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  project_status.py
#  
import sys
import os
from pathlib import Path
import yaml

import logging
logger = logging.getLogger(__name__)

def write_markdown(content, filepath, header=None):
    
    if type(content) is list:
        content = "\n\n".join(content)

    if header:
        content = f'---qq{yaml.dump(header, default_flow_style=False)}...qq{content}'.replace('qq', "\n")
        
    outfile = Path(filepath)
    
    outfile.write_text(content)
    
        
    
    
