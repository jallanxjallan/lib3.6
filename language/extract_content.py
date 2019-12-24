#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  extract_sentences.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@jeremy-Latitude-E6220>

import sys
import os

from textblob import TextBlob
from bs4 import BeautifulSoup

def extract_text_from_html(html):
    tree = BeautifulSoup(html, 'lxml')
    body = tree.find('body')
    if not body:
        return None
    for tag in body.find_all(['script', 'style', 'ul']):
        tag.decompose()
        
    for em in body.find_all('em'):
        text = next(em.stripped_strings, None)
        if text:
            em.replace_with('*' + text + '*')
            
    for text in [t.get_text(separator='|', strip=True) for t in body.find_all()]:
        yield text


def filter_full_sentences(text):
    blob = TextBlob(str(text))
    for sentence in blob.sentences:
        nouns = [n[0] for n in sentence.tags if n[1][:2] == 'NN']
        verbs = [n[0] for n in sentence.tags if n[1][:2] == 'VB']
        if len(nouns) > 0 and len(verbs) > 0:
            yield str(sentence)
        
def extract_named_entities(text):
    blob = TextBlob(text)
    named_entity = []
    for pos in blob.tags:
        if pos[1].startswith('NNP'):
            named_entity.append(pos[0])
        elif len(named_entity) > 0:
            yield ' '.join(named_entity)
            named_entity = []


