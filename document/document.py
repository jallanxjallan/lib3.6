#!/home/jeremy/Scripts/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr
from pathlib import Path
import json
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE
from textblob import TextBlob

@attr.s
class Document():
    content = attr.ib(default=None)
    metadata = attr.ib(default=None,
            converter=attr.converters.optional(dict))

    @property
    def blob(self):
        return TextBlob(self.content)

    @property
    def words(self):
        return len(self.blob.words)

    def __getattr__(self, attr):
        if attr in self.metadata:
            return self.metadata[attr]

    def __str__(self):
        return '\n'.join(self.content)

    @classmethod
    def read_document(cls, filepath=None, text=None, format='markdown'):

        cmds = ['pandoc',
                '--to=markdown',
                '--lua-filter=export_meta.lua'
                ]
        proc_parms = dict(stdout=PIPE, stderr=PIPE, universal_newlines = True)
        com_parms = dict(timeout=5)

        if filepath:
            cmds.append(str(filepath))
        elif text:
            cmds.append(f'--from={format}')
            proc_parms['stdin']= PIPE
            com_parms['input'] = text

        p = Popen(cmds, **proc_parms)

        rs = p.communicate(**com_parms)
        metadata = None
        try:
            metadata = json.loads(rs[1])
        except JSONDecodeError as e:
            print(rs[1])

        return cls(content=rs[0], metadata=metadata)

    def write_document(self, outputfile=None, standalone=True, format='markdown', **kwargs):
        cmds = ['pandoc',
                f'--to={format}',
                '--from=markdown',
                ]
        if outputfile:
            cmds.append(f'--output={str(outputfile)}')
        if standalone:
            cmds.append('-s')
        if self.metadata:
            for key, value in self.metadata.items():
                cmds.append(f'--metadata={key}:{value}')
        for key,value in kwargs.items():
            cmds.append(f'--{key}={value}')
        proc_parms = dict(stdin=PIPE, universal_newlines=True)
        content = self.content or "\n"
        com_parms=dict(input=content, timeout=5)
        p = Popen(cmds, **proc_parms)
        rs = p.communicate(**com_parms)
        return rs
