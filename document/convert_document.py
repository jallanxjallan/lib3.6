#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from collections import defaultdict
from uuid import uuid4
from tempfile import TemporaryDirectory
import logging
from pathlib import Path
import yaml
import subprocess

sys.path.append('/home/jeremy/Library/')
from utility.config import load_config

DEFAULT_FORMAT = 'markdown'
filter_path = Path('/home/jeremy/Library/document/filters')

def pandoc_format_map(filepath):
    """Return output format for source filename"""
    mapping = dict(
        md=DEFAULT_FORMAT,
        txt=DEFAULT_FORMAT,
        pdf='context'
    )

    fp = Path(filepath) if type(filepath) is str else filepath
    suffix = fp.suffix.lstrip('.')
    return mapping.get(suffix, suffix)

def format_arguments(kwargs):
    args = {}

    if kwargs.get('filters'):
        args['filters'] = [str(filter_path.joinpath(f).with_suffix('.py')) for f in kwargs['filters']]



    if kwargs.get('extensions'):
        args['to' output += '+' + '+'.join((e for e in kwargs['extensions']))

    return output, {k:v for k,v in keyword_args.items()}

def text_to_text(text, input_format=None, output_format=None, **args):
        pass

def text_to_file(text, input_format=None, **args):
        pass

def file_to_text(filepath, output_format=None, **args):
        pass

def file_to_file(input_filepath, output_filepath, **args):
        pass

def files_to_files(input_filepaths, output_filepaths, **args):
        pass

def files_to_file(input_filepaths, output_filepath, args):
        pass


def convert_text(source_text, target, **args):
    if type(source_text) is list:
        source_text = '\n\n'.join(source_text)
    if not 'to' in args:
        kwargs['to'] = DEFAULT_FORMAT

    args['text'] = source_text

    args = format_arguments(kwargs)
    if target == 'text':

    output, keyword_args =

    try:
        rs = pypandoc.convert_text(source_text, output, **keyword_args)
    except Exception as e:
        logging.info(e)
        return False
    return rs.strip("\n")

def convert_file(source_filepath, *target, **kwargs):
    output, keyword_args = format_arguments(target, kwargs)

    try:
        rs = pypandoc.convert_file(str(source_filepath), output, **keyword_args)
    except FileNotFoundError:
        logging.info(f'unable to import {source}')
        return False
    except RuntimeError as e:
        logging.info(f'unable to import {source}')
        return False
    except Exception as e:
        logging.info(f'unable to import {source}')
        return False
    if rs == '':
        return target
    return rs

def run_converter(input, output=None):
    def write_args_file(args):
        __, args = format_arguments(args['output-file'], args)
        arg_filepath = Path(tmpdir, uuid4().hex).with_suffix('.yaml')
        with arg_filepath.open('w') as outfile:
            yaml.dump(args, outfile)
        print(f'pandoc -d {str(arg_filepath)}', file=batch_file)



    with TemporaryDirectory() as tmpdir:
        batch_filepath = Path(tmpdir, 'batch_file.sh')
        output_files = []
        with batch_filepath.open('w') as batch_file:
            for arg_item in input_args:
                input_suffix = Path(arg_item['input-file']).suffix
                if not 'output-file' in arg_item:
                    arg_item['output-file'] = str(Path(tmpdir, uuid4().hex).with_suffix(input_suffix))
                    output_files.append(arg_item['output-file'])
                write_args_file(arg_item)
            if output_args:
                output_args['input-files'] = output_files
                write_args_file(output_args)
        subprocess.run(['bash', str(batch_filepath)])
        if output and 'text' in output:
            return Path(output['output-file']).read_text()
        else:
            return True
