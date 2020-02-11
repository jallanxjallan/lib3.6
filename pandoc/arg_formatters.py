#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr

filter_folder = Path('/home/jeremy/Library/pandoc')

def format_args(func):
    def wrapper(source, *output, **kwargs):
                        
        keyword_wargs = defaultdict(list)
        
        if kwargs.get('filters']:
            for filter_name in kwargs['filters']:
                f = Path(filter_name)
                keyword_wargs['filters'].append(str(filter_folder.joinpath(f).with_suffix('.py'))

        if kwargs.get('metadata']:
            for k,v in metadata.items():
                keyword_wargs['extra_args'].append(f'--metadata={k}:{v}')
        
        if len(output) > 0:
            if output[0] in pypandoc.get_pandoc_formats():
                output = output[0]
            else:
                keyword_wargs['outputfile'] = outputfile[0]
                output = None
        
        kwargs = {k:v for k,v in keyword_args.items()}
        return method(source, output, **kwargs)
    return wrapper
