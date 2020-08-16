#!/usr/bin/env python
# coding: utf-8

import sys
from subprocess import run, Popen, PIPE
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path
import attr

sys.path.append('/home/jeremy/Library')

from document.md_document import MDDocument

CWD = Path.cwd()
INTER_PREFIX = 'inter'
INTER_SUFFIX = '.md'


@attr.s
class InputArgs():
    compile_path = attr.ib(default=None)
    seq = attr.ib(default=None)
    input_path = attr.ib()
    output_path = attr.ib()
    defaults_path = attr.ib(default='generic')

    @input_path.default
    def _temp_glob(self):
        return str(self.compile_path.joinpath(f'{INTER_PREFIX}*').with_suffix(INTER_SUFFIX))

    @output_path.default
    def _sequenced_temp_file(self):
        return str(self.compile_path.joinpath(f'{INTER_PREFIX}_{str(self.seq).zfill(5)}').with_suffix(INTER_SUFFIX))

    def __str__(self):
        return ','.join((str(self.input_path), str(self.output_path), str(self.defaults_path)))


def convert_interfile(inputs, output, defaults):
    data_path = CWD
    output_filepath = CWD.joinpath(output)
    output_defaults_path = data_path
    input_objs = []

    with TemporaryDirectory() as compile_dir:
        compile_path = Path(compile_dir)
        for seq, input in enumerate(inputs):
            try:
                input_objs.append(InputArgs(
                    compile_path=compile_path,
                    seq=seq,
                    input_path=input[0].filepath,
                    defaults_path=input[1]))
            except Exception as e:
                print(e)
                continue


        input_objs.append(InputArgs(
            compile_path=compile_path,
            output_path=output,
            defaults_path=defaults
        ))
        input_objs.append(',,')
        input_args = '\n'.join([str(i) for i in input_objs])
        command_args = ';'.join(["IFS=','",
            "while read input output defaults", "do pandoc --defaults=$defaults --output=$output $input", "done"])
        p = Popen(command_args, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
        rs = p.communicate(input=input_args, timeout=60)

        return rs
