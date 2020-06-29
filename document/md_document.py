#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
import attr

import logging
logger = logging.getLogger(__name__)

from .yaml_document import load_yaml, dump_yaml

def split_text(text):
    try:
        metadata, content = text.split('---')[1:]
    except ValueError:
        content = text
        metadata = None
    return metadata, content

@attr.s
class MDDocument():
    content = attr.ib()
    metadata = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: load_yaml(x)))
    filepath = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: str(x)))

    def write_file(self, filepath=None):
        texts = []
        if self.metadata:
            texts.append(dump_yaml(self.metadata))
        texts.append(self.content)

        text = '\n'.join(texts)

        if filepath:
            outfile = Path(filepath)
            outfile.write_text(text)
        else:
            return text

    def __str__(self):
        return self.content

    def __getattr__(self, att):
        if self.metadata:
            return self.metadata.get(att)
        else:
            return None

def read_file(filepath):
    fp = Path(filepath) if type(filepath) is str else filepath
    if not fp.exists():
            return False
    elif not fp.is_file():
        return False
    elif not fp.suffix == '.md':
        return False
    text = fp.read_text()
    metadata, content = split_text(text)
    return MDDocument(content, metadata, filepath)

def read_text(text):
    metadata, content = split_text(text)
    return MDDocument(content, metadata)
