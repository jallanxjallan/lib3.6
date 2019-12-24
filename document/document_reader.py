#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from pathlib import Path
import pypandoc

from document import Document
#~ from document import parse_pdf_document

import logging
logger = logging.getLogger(__name__)

DOCUMENT_SOURCE = 'document_source'


def read_zipfile(filepath):
    try:
        zipfile = ZipFile(filepath)
    except ZipFileError:
        logger.info(f'unable to import {filepath}')
        return False
    for zip_object in zipfile:
        yield read_file(zip_obj)
    return True

def read_files(source):    
    if type(source) is str:
        source = Path(source)
    if not source.exists():
        logger.info(f'unable to import {str(source)}')
        return False

    if source.isdir():
        for filepath in source.iterdir():
            doc = Document(read_file(filepath))
            doc.meta[DOCUMENT_SOURCE]= filepath
            yield doc
    elif source.suffix == '.zip':
        for zip_obj in read_zipfile(source):
            doc = Document(read_text(zip_obj))
            doc.meta[DOCUMENT_SOURCE]= zip_obj.name
            yield doc
    elif source.suffix == '.pdf':
        for page in parse_pdf_document(source):
            for text_box in page.text_boxes():
                doc = Document(read_text(zip_obj))
                doc.meta[DOCUMENT_SOURCE]= source
                yield doc
    else:
        doc = Document(source)
        doc.meta[DOCUMENT_SOURCE]= source
        yield doc
        
        
                
