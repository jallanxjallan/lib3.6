#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr
import types
from pathlib import Path
from urllib.parse import urlparse


@attr.s
class SourceItem():
    content = attrib.ib(default=None)
    filename = attrib.ib(default=None)
    source = attrib.ib(default='file') # options are zip, pdf, web, text

def get_url(url):
    try:
        return request.get(source).text
    except Exception as e:
        print('http error', e)
    return False
    


def source_type(source):
    parsed = urlparse(source)
    
    if parsed.scheme == 'http' or parsed.scheme == 'https': # source is a url
        yield get_url(source)
    
    elif parsed.scheme == 'file': # source has a file schema
        yield Path(source) # so flagged as filepath in calling function
   
    fp = Path(source)  # source might be a local file
    
    if fp.is_file(): # source is a single file
        if fp.suffix == '.pdf': # parse pdf and return raw text of each page
            for no, page in parse_pdf(fp):
                yield SourceItem(content=page.text, filename=f'str({fp})_page_{no}', source='pdf')
        
        elif fp.suffix == '.zip': 
            for item in parse_zip(fp): # open zip and return 
                yield SourceItemcontent=item.contebnt, filename=item.filename)
        else:
            yield SourceItem(filepath = fp)
    elif fp.is_dir:
        for filepath in fp.iterdir():
            yield SourceItem(filepath = filepath)
    yield SourceItem(content = source)
    
    

def parse_source(source):
    if type(source) is list or type(source) is types.GeneratorType:
        for item in source:
            yield source_type(item)
    else:
        yield source_type(item)


