#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2020 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import re
from pathlib import Path
import spacy
from textacy.preprocessing.normalize import normalize_whitespace

sys.path.append('/home/jeremy/Library')

nlp = spacy.load('en_core_web_sm')
# sentencizer = nlp.create_pipe("sentencizer")
# nlp.add_pipe(sentencizer, first=True)

block_pat = re.compile(r"\|(.+?)\|")

def extract_text_content(soup):
    [x.extract() for x in soup.findAll(['script', 'style'])]
    return '|'.join([p.get_text() for p in soup.body.findAll('p')])

def extract_text_blocks(doc):
    print(doc)
    for match in block_pat.finditer(doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)
        if span is not None:
            yield span
        else:
            yield False

def extract_webpage_text_content(soups):
    docs = nlp.pipe([extract_text_content(s) for s in soups])
    for doc in docs:
        yield filter(None, [b for b in extract_text_blocks(doc)])
