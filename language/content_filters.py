#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  entity_extractor.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import spacy
from textblob import TextBlob
from spacy.matcher import Matcher
from spacy.attrs import POS



nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)



def min_word_count(text, word_count=10):
    blob = TextBlob(text)
    if len(blob.words) > word_count:
        return True
    return False
    

def has_valid_sentences(text):
    matcher.add("Noun Verb Noun", [[{"POS": {"REGEX": "NN*"}}, ]{{"POS": {"REGEX": "VB*"}}, {"POS": {"REGEX": "NN*"}}])

    doc = nlp(text, disable= ['vectors', 'textcat',  'ner'])
    for token in doc:
        yield (token.text, token.pos_)
    

