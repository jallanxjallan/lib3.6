#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from pathlib import Path
import attr
import re
from tempfile import NamedTemporaryFile
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)

from textblob import TextBlob

from .yaml_document import load_yaml, dump_yaml

split_pat = re.compile(r'-{3}\n')

def _parse_document(text):
    parts = split_pat.split(text, maxsplit=2)
    try:
        data = dict(metadata=parts[1], content=parts[2])
    except IndexError:
        data = dict(content=parts[0])
    return data

def _handle_yaml(m):
    if type(m) is str:
        m = load_yaml(m)
    M = attr.make_class("MDATA", [k for k in m])
    return M(*m.values())


@attr.s
class MDDocument():
    content = attr.ib(default=None)
    metadata = attr.ib(default=None,
            converter=attr.converters.optional(_handle_yaml))
    filepath = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: Path(x)))
    tempfile = attr.ib(default=False)
    overwrite = attr.ib(default=False)
    blob = attr.ib(default=False)

    @property
    def blob(self):
        return TextBlob(self.content)

    def _make_document(self):
        texts = []
        if self.metadata:
            texts.append(dump_yaml(attr.asdict(self.metadata)).replace('...', '---'))
        if self.content:
            texts.append(str(self.content))
        else:
            texts.append('\n')
        if len(texts) > 0:
            self.text = '\n'.join(texts)
        else:
            self.text = None

    def write_file(self):
        self._make_document()
        if self.tempfile:
            self.fp = NamedTemporaryFile(suffix='.md')
            self.filepath = Path(self.fp.name)
        try:
            self.filepath.write_text(self.text)
        except Exception as e:
            print(e)
            return False
        return self.filepath

    def __str__(self):
        self._make_document()
        return self.text

    def __getattr__(self, att):
        if self.metadata:
            return getattr(self.metadata, att)
        else:
            return None

    @classmethod
    def read_file(cls, filepath):
        fp = Path(filepath) if type(filepath) is str else filepath
        if not fp.suffix == '.md':
            print(fp, 'not a markdown file')
            raise FileNotFoundError
        try:
            text = fp.read_text()
        except FileNotFoundError:
            print(fp, 'not found')
            raise
        return cls(filepath=fp, **_parse_document(text))

    @classmethod
    def read_text(cls, text):
        return cls(filepath=fp, **_parse_document(text))
