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
from nltk import RegexpParser
from nltk import Tree
from textblob import TextBlob

# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NNP\w?>)+.*<NNP\w?>}"
chunker = RegexpParser(NP)

def get_named_entities(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunks = []
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunks:
                continuous_chunks.append(named_entity)
                current_chunk = []
        else:
            continue

    if len(continuous_chunks) > 0:
        return continuous_chunks
    return None
    
def get_full_sentences(text):
    for sent in [s for s in TextBlob(text).sentences]:
        nouns = [n[0] for n in sentence.tags if n[1][:2] == 'NN']
        verbs = [n[0] for n in sentence.tags if n[1][:2] == 'VB']
        if len(nouns) > 0 and len(verbs) > 0:
            yield str(sentence)

def page_number():
     @property
    def page_number(self):
        bottom_line = next((c for c in self.text_chunks() if c.component  == 'footer'), None)
        if not bottom_line:
            return None
        return ''.join([d for d in bottom_line.text if d.isdigit()])
