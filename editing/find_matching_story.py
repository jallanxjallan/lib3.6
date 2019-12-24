#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
import operator
import plac
from pathlib import Path
from lxml import etree
from lxml.etree import XMLSyntaxError
from bs4 import BeautifulSoup
import spacy
from document.text_document import read_document, write_document
import textacy
import textacy.preprocessing as tp
import pandas as pd
from fuzzywuzzy import fuzz
import pypandoc


DF_COLUMNS = ['filepath', 'document']

nlp = spacy.load('en_core_web_sm')


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
    
#~ def parse_text_paras(content):
    #~ content = BeautifulSoup(pypandoc.convert_file(filepath, 'html', format='markdown'), 'lxml')
    #~ for para in content.find_all('p'):
        #~ yield para.get_text()
        
#~ def parse_files(project_path, component, parser):
    #~ source_dir = Path(project_path, component)
    #~ for filepath in source_dir.iterdir():
        #~ texts = [i for i in parser(str(filepath))]
        #~ for doc in nlp.pipe([t for t in texts if not t is None]):
            #~ yield (filepath.stem, doc)
                    
#~ parsers = dict(stories=parse_story_file, content=parse_content_file)             




#~ def match_content(ents, dfs):
    #~ if len(ents) == 0:
        #~ return 0
    #~ matches = [(len(ents.intersection(i.entities)) / len(ents), i.filepath) for i in dfs.itertuples()]
    #~ return max(matches, key=operator.itemgetter(0))[1]
    

def main(filepath):
    for para in parse_icml_content(filepath):
        print('-', para)


if __name__ == '__main__':
    plac.call(main)
    
