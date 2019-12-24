#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  entity_extractor.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from collections import defaultdict
from nltk import word_tokenize, sent_tokenize, pos_tag, ne_chunk
from nltk.corpus import names
import pandas as pd

name_list = [(n.lower(),g) for g in ('male', 'female') for n in names.words('{}.txt'.format(g))]

df_names = pd.DataFrame(name_list, columns=['name', 'gender'])

def get_gender(name):
    return df_names[df_names.name == name].gender.values[0]



def modify_sentence(text, mapping):
    words = word_tokenize(text)
    tagged = pos_tag(words)
    sentence = ' '.join([mapping.get(t[1], t[0]) for t in tagged])
    
    return sentence
    
