#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
from operator import itemgetter
import itertools
import attr

import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher

sys.path.append('/home/jeremy/Library')
from utility.helpers import lazyloader

@attr.s
class Doc():
    doc = attr.ib()
    
    def __attrs_post_init__(self):
        if type(self.doc) is str:
             self.doc = self.nlp(self.doc)
        self.length = len(self.doc)
        self.center = int(self.length / 2)
        self.text = self.doc.text
        
    @lazyloader
    def nlp(self):
        return spacy.load('en_core_web_sm', disable=['ner', 'pos', 'parser'])
        
    @property
    def words(self):
        return [w for w in self.doc if self.word_filter(w)]
    
    def segment(self, start, end, new_doc=False):
        start = 0 if start < 0 else start
        end = self.length if end > self.length else end
        seg = self.doc[start:end]
        if new_doc:
            return self.nlp(seg.text)
        return seg
        
    def word_filter(self, w):
        if w.is_stop:
            return False
        if w.is_punct:
            return False
        return True
        
        
def match_text_passage(passage, document):
    def find_anchors(anchor):
        if anchor == 'head':
            anchor_text = p.doc[0:2].text
            anchor_index = 0
            doc_anchor = int(b.left)
        else:
            anchor_text = p.doc[-3:-1].text
            anchor_index = -1
            doc_anchor = int(b.right)
        anchor_pat = re.compile(re.escape(anchor_text))
        
        matches = []
        for match in re.finditer(anchor_pat, d.text):
            anchor = match.span()
            span = d.doc.char_span(*anchor) 
            span_anchor = span[anchor_index].i
            doc_anchor = d.doc[anchor_index].i
            matches.append((doc_anchor,  abs(span_anchor - doc_anchor)))
        print('matches', matches)    
        return  min(matches, key=itemgetter(1))[0]
    
    d = Doc(document)
    p = Doc(passage)
    
    df = pd.DataFrame([(p[1].i) \
        for p in itertools.product(p.words,d.words) if p[0].text == p[1].text ], \
        columns=['offset'])
          
    bin_size = len(d.words) / len(p.words)
    
    g = pd.cut(df['offset'], bins=bin_size).value_counts()
    b = next(k for k,v in g.items() if v == g.max())
    start = find_anchors('head')
    end = find_anchors('tail')
    return d.segment(start,end)
    

        
  
