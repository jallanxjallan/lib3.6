#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  project_status.py
#  
import sys
import os
from pathlib import Path
import pypandoc


import logging
logger = logging.getLogger(__name__)

FILE_FORMATS = dict(
    md='markdown_mmd',
    txt='plain'
)

DEFAULT_FORMAT = 'markdown'

def convert_to_string(text):
    if type(text) is list:
        return '\n\n'.join(text)
    else:
        return text

def get_file_format(filepath):
    suffix = filepath.suffix[1:]
    try:
        return FILE_FORMATS[suffix]
    except KeyError:
        return suffix
        
def file_args(filepath, input_format, extra_args):
    output_format = get_file_format(filepath)
    args = dict(format=input_format, to=output_format, outputfile=str(filepath)) 
    if output_format == 'pdf':
        args['extra_args'] = ["--latex-engine=pdflatex"]

    elif output_format == 'rtf':
        args['extra_args']=['--standalone']
    elif extra_args:
        args['extra_args']=extra_args
    return args

def text_to_text(text, input_format=DEFAULT_FORMAT, output_format=DEFAULT_FORMAT):
    try:
        return pypandoc.convert_text(convert_to_string(text), output_format, format=input_format)
    except Exception as e:
        logger.info('unable to convert text' )
        return False
    
def file_to_text(filepath, output_format=DEFAULT_FORMAT):
    filepath = Path(filepath) if type(filepath) is str else filepath
    try:
        return pypandoc.convert_file(str(filepath), output_format, format=get_file_format(filepath))
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False
    except RuntimeError as e:
        print(e)
        return False

def text_to_file(text, filepath, extra_args=None, input_format=DEFAULT_FORMAT):
    filepath = Path(filepath) if type(filepath) is str else filepath
    args = file_args(filepath, input_format, extra_args)
    try:
        return pypandoc.convert_text(convert_to_string(text), **args)
    except FileNotFoundError:
        logger.info(f'unable to export tp {filepath}')
        return False
        
def file_to_file(infile, outfile):
    infilepath = Path(infile) if type(infile) is str else infile
    outfilepath = Path(outfile) if type(outfile) is str else outfile
    
    args = file_args(outfilepath, get_file_format(infilepath))
    try:
        return pypandoc.convert_file(str(infilepath), **args)
    except FileNotFoundError:
        logger.info(f'unable to export tp {filepath}')
        return False
