#!/usr/bin/env python
# coding: utf-8

from subprocess import run, Popen, PIPE
from tempfile import TemporaryDirectory
from pathlib import Path

def convert_many_to_one(input, output, output_defaults=None, data_dir=None):
    with TemporaryDirectory() as tmpdir:
        tmppath = Path('staging')
        input.append(('','',''))
        input_args = '\n'.join([','.join((a[0], f'{str(tmppath.joinpath(a[1]))}', a[2])) for a in input])
        command_args = ["IFS=',';",
                        "while read infile outfile defaults; do pandoc"]
        if data_dir:
            command_args.append(f'--data-dir={data_dir}')
        command_args.append('--defaults=$defaults --output=$outfile $infile; done')

        arg_string = ' '.join(command_args)
        print(arg_string)
        p = Popen(arg_string, stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
        c = p.communicate(input=input_args, timeout=5)
        print(c)
        output_args = ['pandoc']
        if data_dir:
            output_args.append(f'--data-dir={data_dir}')
        if output_defaults:
             output_args.append(f'--defaults={output_defaults}')

        output_args.append(f'--output={output}')
        output_args.extend(['staging/001.md', 'staging/002.md', 'staging/003.md'])
        rs = run(output_args)

        print(rs)
