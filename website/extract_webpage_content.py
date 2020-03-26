#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2020 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import spacy
from textacy.preprocessing.normalize import normalize_whitespace

sys.path.append('/home/jeremy/Library')

from document.convert_document import convert_text

nlp = spacy.load('en_core_web_sm')
# sentencizer = nlp.create_pipe("sentencizer")
# nlp.add_pipe(sentencizer, first=True)

def extract_text_content(soup):
    [x.extract() for x in soup.findAll(['script', 'style'])]
    t1 = soup.body.get_text()
    t2 = re.sub(r'\n{2:}', ' ', t1)
    t3 = normalize_whitespace(t2)
    return t3

def is_proper_sentence(s):
    return True
    if s.text.endswith('.'):
        return True
    return False

def extract_webpage_content(url):
    try:
        page = requests.get(url)
    except:
        print(f'Unable to load page {url}')
        return False

    soup = BeautifulSoup(page.text, 'lxml')

    text = extract_text_content(soup)

    doc = nlp(text)
    content = [s.text for s in doc.sents if is_proper_sentence(s)]
    return convert_text(content)
