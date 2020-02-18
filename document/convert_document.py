#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from collections import defaultdict
import logging
from pathlib import Path
import pypandoc

DEFAULT_FORMAT = 'markdown'

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
    keyword_args['encoding'] = 'UTF-8'
    for k,v in kwargs.items():
        keyword_args[k] = v
    if not output in pypandoc.get_pandoc_formats()[1]:
        keyword_args['outputfile'] = str(output)
        keyword_args['extra_args'].append('--standalone')
        output = pandoc_format_map(output)


    if kwargs.get('filters'):
        for filter_name in kwargs['filters']:
            f = Path(filter_name)
            keyword_args['filters'].append(str(filter_folder.joinpath(f).with_suffix('.py')))

    if kwargs.get('metadata'):
        for k,v in metadata.items():
            keyword_args['extra_args'].append(f'--metadata={k}:{v}')

    if kwargs.get('extensions'):
        output += '+' + '+'.join((e for e in kwargs['extensions']))

    return output, {k:v for k,v in keyword_args.items()}


def convert_text(source_text, *target, **kwargs):
    if not 'format' in kwargs:
        kwargs['format'] = DEFAULT_FORMAT
    output, keyword_args = format_arguments(target, kwargs)

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
    return rs
