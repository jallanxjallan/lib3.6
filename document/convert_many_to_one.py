#!/usr/bin/env python
# coding: utf-8

from subprocess import run, Popen, PIPE
from tempfile import TemporaryDirectory
from pathlib import Path
cwd = Path.cwd()

def make_input_arg(input):
    input_file = str(cwd.joinpath(input['filepath']))
    input_defaults = input.get('defaults') or 'generic'
    return ','.join((input_defaults, input_file))

def convert_many_to_one(inputs, output_file, output_defaults='generic', data_dir=str(cwd)):
    input_args = '\n'.join([make_input_arg(a) for a in inputs])
    input_args += '\n,'

    command_args = f'convert_many_to_one.sh {output_file} {output_defaults} {data_dir}'
    p = Popen(command_args, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
    rs = p.communicate(input=input_args, timeout=5)
    print(rs)
