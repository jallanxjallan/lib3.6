#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from pathlib import Path
import attr

from ruamel.yaml import YAML

import logging
logger = logging.getLogger(__name__)

yaml = YAML()
yaml.explicit_start = True
yaml.explicit_end = True

@attr.s
class Document():
    metadata = attr.ib()
    content = attr.ib()

    def __attrs_post_init__(self):
        try:
            mdata = yaml.load(self.metadata)
        except Exception as e:
            print(e)
            return
        for k, v in mdata.items():
            setattr(self, k, v)

def read_document(filepath):
    try:
        fp = Path(filepath)
    except FileNotFoundError:
        return False

    text = fp.read_text()

    try:
        metadata, content = text.split('---')[1:]

    except ValueError:
        metadata = {}
        content = text
    
    return Document(metadata, content)
