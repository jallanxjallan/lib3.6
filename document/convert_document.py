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


def format_kwargs(**kwargs):
    keyword_args = defaultdict(list)

    keyword_args['format'] = 'markdown'

    if kwargs.get('filters'):
        for filter_name in kwargs['filters']:
            f = Path(filter_name)
            keyword_args['filters'].append(str(filter_folder.joinpath(f).with_suffix('.py')))

    if kwargs.get('metadata'):
        for k,v in metadata.items():
            keyword_args['extra_args'].append(f'--metadata={k}:{v}')

    if len(output) > 0:
        if output[0] in pypandoc.get_pandoc_formats():
            output = output[0]
        else:
            keyword_args['outputfile'] = output[0]
            output = None

    output = 'markdown'
    kwargs = {k:v for k,v in keyword_args.items()}
    return str(source), output, **kwargs


@format_args
def convert_text(source, output, **kwargs):
    print('output', output)
    print('kwargs', kwargs)

    rs = pypandoc.convert_text(source, output, **kwargs)
    #~ try:
        #~ rs = pypandoc.convert_text(source, output, **kwargs)
    #~ except Exception as e:
        #~ logging.info(e)
        #~ return False
    #~ if outputfile:
        #~ return True
    return rs

@format_args
def convert_file(source, output, **kwargs):
    rs = pypandoc.convert_file(source, output, **kwargs)
    #~ try:

    #~ except FileNotFoundError:
        #~ logging.info(f'unable to import {source}')
        #~ return False
    #~ except RuntimeError as e:
        #~ logging.info(f'unable to import {source}')
        #~ return False
    #~ except Exception as e:
        #~ logging.info(f'unable to import {source}')
        #~ return False
    #~ if outputfile:
        #~ return True
    #~ return rs
    if len(rs) > 5:
        return rs
    return True
