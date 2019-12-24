#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr
from pathlib import Path

from document import Document
from document.pdf_document import parse_pdf_document

import logging
logger = logging.getLogger(__name__)

MARKDOWN = 'markdown_mmd'


def read_file(filepath):
    try:
        return pypandoc.convert_file(str(filepath), MARKDOWN)
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False
        
        
def read_text(text):
    try:
        return pypandoc.convert_text(str(filepath), MARKDOWN)
    except FileNotFoundError:
        logger.info(f'unable to import {filepath}')
        return False

def read_zipfile(filepath):
    try:
        zipfile = ZipFile(filepath)
    except ZipFileError:
        logger.info(f'unable to import {filepath}')
        return False
    for zip_object in zipfile:
        yield read_file(zip_obj)
    return True

def document_reader(source):
    if type(source) is str:
        source = Path(source)
    if not source.exists():
        logger.info(f'unable to import {str(source)}')
        return False
        
    if source.isdir():
        for filepath in source.iterdir():
            doc = Document(read_file(filepath))
            #~ doc.meta[DOCUMENT_SOURCE]= filepath
            yield doc
    elif source.suffix == 'zip':
        pass
        #~ for zip_obj in read_zipfile(source):
            #~ doc = Document(read_text(zip_obj))
            #~ doc.meta[DOCUMENT_SOURCE]= zip_obj.name
            #~ yield doc
    elif source.suffix == 'pdf':
        pass
        #~ for page in parse_pdf_document(source):
            #~ for text_box in page.text_boxes():
                #~ doc = Document(read_text(zip_obj))
                #~ doc.meta[DOCUMENT_SOURCE]= source
                #~ doc.meta[PAGENO]= page.pageno
                #~ doc.meta[COMPONENT]= text_box.component
                #~ yield doc
    else:
        yield Document(read_file(source))
return True
    
    
