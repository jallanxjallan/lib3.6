#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
import attr
import re

import logging
logger = logging.getLogger(__name__)

from .yaml_document import load_yaml, dump_yaml

split_pat = re.compile('-{3}')

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
    if not fp.suffix == '.md':
        print(fp, 'not a markdown file')
        raise FileNotFoundError
    try:
        text = fp.read_text()
    except FileNotFoundError:
        print(fp, 'not found')
        raise
    parts = split_pat.split(text, maxsplit=2)
    try:
        return MDDocument(parts[2], parts[1], filepath)
    except Exception as e:
        print(e)
        return None


def read_text(text):
    metadata, content = split_text(text)
    return MDDocument(content, metadata)
