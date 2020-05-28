#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
import attr

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

import logging
logger = logging.getLogger(__name__)

yaml = YAML()
yaml.explicit_start = True
yaml.explicit_end = True
yaml.default_flow_style = False


def dump_yaml(data):
    stream = StringIO()
    yaml.dump(data, stream)
    stream.seek(0)
    return stream.read()

def split_text(text):
    try:
        metadata, content = text.split('---')[1:]
    except ValueError:
        content = text
        metadata = None
    return metadata, content

@attr.s
class Document():
    content = attr.ib()
    metadata = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: yaml.load(x)))

    def write_document(self, filepath=None):
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

    def __getattr__(self, att):
        if self.metadata:
            return self.metadata.get(att, None)
        else:
            return None

def read_file(filepath):
    fp = Path(filepath)
    if not fp.exists():
        return f'{fp} does not exist'
    metadata, content = split_text(fp.read_text())
    return Document(content, metadata)

def read_text(text):
    metadata, content = split_text(text)
    return Document(content, metadata)
