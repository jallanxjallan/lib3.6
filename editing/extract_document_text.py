#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import csv
from pathlib import Path
import plac

from textacy.preprocessing import normalize_quotation_marks as nqm


sys.path.append('/home/jeremy/Library')

from document.pdf_document import parse_pdf_document
from document.text_document import file_to_text

def preprocess_text(text):
    return text


def extract_document_text(document_list, output_format='markdown'):
    for document in [Path(d) for d in document_list]:
        if document.suffix == '.pdf':
            for page in parse_pdf_file(str(document)):
                for text_box in page.text_boxes:
                    yield preprocess_text(text_box.text)
        else:
            yield preprocess_text(read_document(str(document)))
                    
if __name__ == '__main__':
    plac.call(extract_document_text)
    
