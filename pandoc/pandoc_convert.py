#!/usr/bin/env python
# coding: utf-8

import sys
from subprocess import run, Popen, PIPE
from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path
import attr

INTER_PREFIX = 'inter'
INTER_SUFFIX = '.md'

@attr.s
class PandocArgs():
    input = attr.ib(default=None)
    output = attr.ib(default=None)
    metadata = attr.ib(default=None)
    standalone = attr.ib(default=True)
    defaults = attr.ib(default=None)
    extra_args = attr.ib(default=None)
    seq = attr.ib(default=None)

def format_args(arg_obj):
    args = []

    if arg_obj.defaults:
        args.append(f'--defaults={arg_obj.defaults}')

    if arg_obj.metadata:
        for k,v in arg_obj.metadata.items():
            args.append(f'--metadata={k}:{v}')

    if arg_obj.extra_args:
        for k,v in arg_obj.extra_args.items():
            args.append(f'{k}={v}')

    return args

def run_converter(arg_streams):
    arg_strings = '\n'.join([' '.join(a) for a in arg_streams])
    p = Popen(['xargs', 'pandoc'], stdin=PIPE, stdout=PIPE, shell=True, universal_newlines=True)
    rs = p.communicate(input=arg_strings, timeout=60)
    return rs

def sequenced_file(seq, base_dir):
    base_dir = Path(base_dir) if type(base_dir) is str else base_dir
    return str(base_dir.joinpath(f'{INTER_PREFIX}_{str(seq).zfill(5)}').with_suffix(INTER_SUFFIX))

def input_glob(base_dir):
    return str(base_dir.joinpath(f'{INTER_PREFIX}_*').with_suffix(INTER_SUFFIX))

def convert_compile(file_args):

    with TemporaryDirectory() as compile_dir:
        compile_path = Path(compile_dir)
        arg_stream = []
        for file_arg in file_args:
            args = format_args(file_arg)
            if file_arg.output:
                args.append(f'--output={file_arg.output}')
            else:
                args.append(sequenced_file(file_arg.seq, compile_path))

            if file_arg.input:
                args.append(file_arg.input)
            else:
                args.append(input_glob(compile_path))
            arg_stream.append(args)
        rs = run_converter(arg_stream)
        print(rs)

def convert_file(file_args):
    args = format_args(file_arg)


# def convert_split(file_args):
#     with TemporaryDirectory() as compile_dir:
#         compile_path = Path(compile_dir)
#
#         input_args = format_args(file_args)
#         input_args.insert(0, '--lua-filter=split_on_header.lua')
#         input_args.insert(1, f'--metadata=compile_dir:{$compile_dir}')
#         rs = run_converter(args)
#         output_args = []
#         for tmpfile in [fp for fp in compile_path.iterdir() if fp.suffix == '.json']:
#             output_file =
#         PandocArgs(
#             input=tmpfile,
#             output=input_args.output
#         )]




#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: filenames from stream target-dir"
  exit 0
fi
tmpdir=$(mktemp -d)
destdir=$1
defaults=$2
while IFS= read srcfile
do
    pandoc \
    --standalone \
     \
     \
    "$srcfile"
done
for tmpfile in $tmpdir/*.json
do
  filename=$(basename "$tmpfile")
  dstfile="${filename%.*}"
  outputfile=$destdir/$dstfile.md
  pandoc --standalone --output=$outputfile $tmpfile
done
# rm -d $tmpdir
