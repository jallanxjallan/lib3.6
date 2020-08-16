#!/usr/bin/env python
# coding: utf-8

from subprocess import run, Popen, PIPE
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path
import attr

sys.path.append('/home/jeremy/Library')

from document.md_document import MDDocument

CWD = Path.cwd()

@attr.s
class TempDoc():
    metadata = attr.ib(default=None)
    content = attr.ib(default=None)
    fp = NamedTemporaryFile(suffix='.md')

    def write_temp_file(self):
        doc = MDDocument(content=self.content,
                         metadata=self.meta,
                         filepath=self.fp.name)
        return doc.write_file()

@attr.s
class InputArgs():
    compile_path = attr.ib(default=None)
    seq = attr.ib(default=None)
    input_path = attr.ib()
    output_path = attr.ib()
    default_path = attr.ib(default='generic')

    @input.default
    def _temp_glob(self):
        return str(self.tmppath.joinpath(f'{INTER_PREFIX}*').with_suffix(INTER_SUFFIX))

    @output.default
    def _sequenced_temp_file(self):
        return str(self.tmppath.joinpath(f'{INTER_PREFIX}_{str(self.seq).zfill(5)}').with_suffix(INTER_SUFFIX))

    def __str__(self):
        return ','.join((self.input, self.output, self.defaults))


def convert_interfile(inputs, output, defaults):
    data_path = CWD.joinpath(data_dir)
    output_filepath = CWD.joinpath(output_file)
    output_defaults_path = data_path.joinpath(data_dir)


    with TemporaryDirectory as compile_dir:
        compile_path = Path(compile_dir)
        for seq, input in enumerate(inputs):
            try:
                input_objs.append(InputArgs(
                    compile_path=compile_path,
                    seq=seq,
                    data_path=data_path,
                    input=input))
            except Exception as e:
                print(e)
                continue
        input_args = '\n'.join([str(i) for i in input_objs])
        command_args = ';'.join(["IFS=','",
            "while read defaults input output do pandoc --defaults=$defaults --output=$outputfile $input done" ])
        p = Popen(command_args, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
        rs = p.communicate(input=input_args), timeout=5)
        return rs
