#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>


import sys
import os
import re
from textblob import TextBlob
from nltk.tag.stanford import StanfordNERTagger
from nltk.parse.corenlp import CoreNLPParser

clean_text = re.compile(r"[!”#$%&’()*+,-./:;<=>?@[\]^_`{|}~]")
delete_pat = re.compile(r'((?<=\~{2})(.*?)(?=\~{2}))')

jar = '/home/jeremy/nltk_data/stanford-ner-2018-10-16/stanford-ner.jar'
model = '/home/jeremy/nltk_data/stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz'

# Prepare NER tagger with english model
ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')

def arg_converter(method):
    def wrapper(arg):
        if not type(arg) is TextBlob:
            text = TextBlob(arg)
        else:
            text = arg
        return method(text)
    return wrapper

@arg_converter
def named_entities(text):
    return ner_tagger.tag(text.words)
