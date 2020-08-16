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

import logging
logger = logging.getLogger(__name__)

from .yaml_document import load_yaml, dump_yaml

split_pat = re.compile('^-{3}|\.{3}$')

@attr.s
class MDDocument():
    content = attr.ib(default=None)
    metadata = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: x))
    filepath = attr.ib(default=None,
            converter=attr.converters.optional(lambda x: Path(x)))
    tempfile = attr.ib(default=False)
    overwrite = attr.ib(default=False)

    def _make_document(self):
        texts = []
        if self.metadata:
            texts.append(dump_yaml(self.metadata).replace('...', '---'))
        if self.content:
            texts.append(self.content)
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
            return self.metadata.get(att)
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
        parts = split_pat.split(text, maxsplit=2)

        if len(parts) > 1:
            try:
                obj = cls(metadata=parts[1], content=parts[2], filepath=fp)
            except Exception as e:
                raise e
        else:
            return obj

    @classmethod
    def read_text(cls, text):
        metadata, content = split_pat.split(text, maxsplit=2)
        try:
            return cls(metadata=metadata, content=content, filepath=fp)
        except Exception as e:
            print(e)
