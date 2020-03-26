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
import pypandoc

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

def format_arguments(target, kwargs):
    try:
        output = target[0]
    except IndexError:
        output = DEFAULT_FORMAT
    keyword_args = defaultdict(list)
    for k,v in kwargs.items():
        keyword_args[k] = v
    if not output in pypandoc.get_pandoc_formats()[1]:
        keyword_args['outputfile'] = str(output)
        keyword_args['extra_args'].append('--standalone')
        output = pandoc_format_map(output)


    if kwargs.get('filters'):
        for filter_name in kwargs['filters']:
            f = Path(filter_name)
            keyword_args['filters'].append(str(filter_path.joinpath(f).with_suffix('.py')))

    if kwargs.get('metadata'):
        for k,v in kwargs['metadata'].items():
            keyword_args['extra_args'].append(f'--metadata={k}:{v}')

    if kwargs.get('extensions'):
        output += '+' + '+'.join((e for e in kwargs['extensions']))

    return output, {k:v for k,v in keyword_args.items()}


def convert_text(source_text, *target, **kwargs):
    if type(source_text) is list:
        source_text = '\n\n'.join(source_text)
    if not 'format' in kwargs:
        kwargs['format'] = DEFAULT_FORMAT
    output, keyword_args = format_arguments(target, kwargs)

    try:
        rs = pypandoc.convert_text(source_text, output, **keyword_args)
    except Exception as e:
        print(e)
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

def combine_files(input_args, output_args=None):
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
