#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  project_status.py
#  

"""
# if string read into uri determine if web page for filename
    # if not, consider it raw text and assume markdown
    # override with format kwarg
    # yield result as class with text kind, filepath, or downloaded web page
    # if generator or list, parse each item and yield
    
    # if outputfile in kwargs determine if fully qualified filename or file path
    # if fullpath, save as that
    # if outfile is directory, save each file with filename taken from source file or url
    # if just raw text, look for name template, else "converted text + digit
    # if multiple text source yield individual strings . Will join at calling function if necessary
"""
import sys
import os
from pathlib import Path

import logging
logger = logging.getLogger(__name__)

from .format_arguments import *

from .converters import *

from .source_processor import source_processor

DEFAULT_FORMAT = 'markdown'

def convert_document(source, 
                        format=DEFAULT_FORMAT
                        to=DEFAULT_FORMAT,
                        filters=None, 
                        metadata=None, 
                        extensions=None,
                        target=None,
                        concatenate=False,
                        zip_file=False
                        ):
    kwargs = defaultdict(list)
    if filters:
        kwargs['filters'] = format_filters(filters)
        
    if metadata:
        kwargs['extra_args'].extend([m for m in format_metadata(metadata)])
    
    if target:
        kwargs['outputfile'] = format_outputfile(target)
    
    
    output = []
    for source_item, filename in source_processor(source):
        if class_name(source_item) == 'PosixPath':
            rs = convert_file(str(source), *args, **kwargs)
        else:
            rs = convert_text(source_item, *args, **kwargs)
        if join_output:
            output.append(rs)
        else:
            yield rs
    if len(output) > 0:
        joined = '\n'.join(output)
        if target:
            convert_text(joined, to, outputfile=kwargs['outputfile'])
        else:
            yield joined
            
                        
    
        

def convert_to_text(source, **kwargs):
    return ' '.join([t for t in text_item in )
        
def convert_to_texts(source, **kwargs):
    for item in convert_document(source, kwargs):
        yield item
        
def convert_to_file(source, outputfile, **kwargs):
    text = convert_to_text(source, kwargs)
    convert_document(text, 



    
    
    
            
    



    

    
    
        
