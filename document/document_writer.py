#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import pypandoc

import logging
logger = logging.getLogger(__name__)





    
'''
def text_to_file(filepath, text, input_format=DEFAULT_FORMAT):
    filepath = Path(filepath) if type(filepath) is str else filepath
    args = file_args(filepath, input_format)
    try:
        return pypandoc.convert_text(convert_to_string(text), **args)
    except FileNotFoundError:
        logger.info(f'unable to export tp {filepath}')
        return False
        
        def file_args(filepath, input_format):
    output_format = get_file_format(filepath)
    args = dict(format=input_format, to=output_format, outputfile=str(filepath)) 
    if output_format == 'pdf':
        args['extra_args'] = ["--latex-engine=pdflatex"]

    elif output_format == 'rtf':
        args['extra_args']=['--standalone']
    return args
'''
    
