#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
import plac
from lxml import etree
from lxml.etree import XMLSyntaxError
import spacy
import textacy
import textacy.preprocessing as tp

#~ def clean_text(text):
    #~ doc = nlp(text)
    #~ for sent in doc.sents:
        #~ yield ' '.join([w.text for w in textacy.extract.words(sent, filter_stops=True, filter_punct=True)])
    
     
def parse_icml_content(filepath):
    tree = etree.parse(filepath)
    contents = []
    for e in tree.getroot().iter('Content', 'Br'):
        if e.tag == "Content":
            contents.append(e.text)
        elif e.tag == 'Br':
            yield ' '.join(contents)
            contents = []
        else:
            pass
    if len(contents) > 0:
        return ' '.join(contents)
    else:
        return True
    
    
def main(filepath):
    for para in parse_icml_content(filepath):
        print('-', para)


if __name__ == '__main__':
    plac.call(main)
    
