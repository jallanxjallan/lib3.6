#!/usr/bin/env python
# coding: utf-8

from subprocess import run, Popen, PIPE
from pathlib import Path
import attr

INTER_PREFIX = 'sequenced_file'
INTER_SUFFIX = '.md'


def sequenced_file(seq, base_dir):
    base_dir = Path(base_dir) if type(base_dir) is str else base_dir
    return str(base_dir.joinpath(f'{INTER_PREFIX}_{str(seq).zfill(5)}').with_suffix(INTER_SUFFIX))

def input_glob(base_dir):
    return str(base_dir.joinpath(f'{INTER_PREFIX}_*').with_suffix(INTER_SUFFIX))

@attr.s
class InputArgs():
    input = attr.ib()
    output = attr.ib()
    defaults = attr.ib(default='generic')

    def __str__(self):
        return ','.join((str(self.input), str(self.output), str(self.defaults)))

def convert_many(inputs):
    input_args = '\n'.join([str(i) for i in inputs])

    command_args = ';'.join(["IFS=','",
        "while read input output defaults", "do pandoc --defaults=$defaults --output=$output $input", "done"])
    p = Popen(command_args, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
    rs = p.communicate(input=input_args, timeout=60)

    return rs
