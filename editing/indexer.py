#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import csv
from pathlib import Path
import plac

import pandas as pd
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from textacy.preprocessing import normalize_quotation_marks as nqm


sys.path.append('/home/jeremy/Library')

from document.pdf_document import parse_pdf_document

DF_COLUMNS = ['page_no', 'box_pos', 'ent_pos', 'label', 'entity', 'sentence'  ]
EL_COLUMNS = ['entity', 'primary', 'index_term', 'pattern']
IN_COLUMNS = ['index_term', 'page_list']
EDIT_SHEETS = dict(new=['entity', 'label', 'sentence'],
                    include=['entity', 'label'],
                    exclude=['entity', 'label'], 
                    make=['entity', 'label', 'term', 'pattern']
                    )

def build_dataframe(nlp, texts):
    print("building dataframe...")
    docs = nlp.pipe([t[2] for t in texts])
    return pd.DataFrame([
            (texts[n][0], texts[n][1], e.start, e.label_, e.text, e.sent.text) \
            for n, d in enumerate(docs) \
            for e in d.ents], columns=DF_COLUMNS) 



def write_entry_lists(nlp, texts, entry_lists, fn):
    print("writing entry lists...")
    df = build_dataframe(nlp, texts)
    
    els = [df for df in entry_lists.values() if len(df.columns) > 0]
    if els:
        new_entries = df[~df.entity.isin(pd.concat(els, sort=True))]
    else:
        new_entries = df
    
    entry_lists['new'] = new_entries[EDIT_SHEETS['new']]
    
    with pd.ExcelWriter(fn) as writer:
        for name, df in entry_lists.items():
            df.to_excel(writer, f'{name}')
        writer.save()
    
def main(pdf_filename, action='write_index_file'):
    nlp = spacy.load('en_core_web_sm')
    pdf_source = Path(pdf_filename)
    texts = [(p.page_no, 'left', nqm(b.text)) for p in parse_pdf_document(pdf_filename) for b in p.text_boxes()]
    entry_list_file = Path(f'{pdf_source.stem}_entry_edit.xlsx')
    if entry_list_file.exists():
        entry_lists = {n:pd.read_excel(entry_list_file, sheet_name=n) for n in EDIT_SHEETS}
    else:
        entry_lists = {n:pd.DataFrame([], columns=ls) for n,ls in EDIT_SHEETS.items()}
    
    if action == 'write_entry_lists':
        write_entry_lists(nlp, texts, entry_lists, entry_list_file)
        
    elif action == 'write_index_file':
        print('writing index file...')
        
        #~ nlp.add_pipe(IndexEntriesComponent(nlp, entry_lists['Make'))
        #~ write_index_file(nlp, texts, entry_lists, index_file)
        

if __name__ == '__main__':
    plac.call(main)
    


'''
class IndexEntriesComponent(object):
    

    name = "index_entries"  # component name, will show up in the pipeline

    def __init__(self, nlp, el):
        """Initialise the pipeline component. The shared nlp instance is used
        to initialise the matcher with the shared vocab. 
        """
        
        self.matcher = Matcher(nlp.vocab)
        self.entity_list = el
        
        for row in [r for r in el.itertuples() if not r.pattern]:
            matcher.add(row.entity, None, row.pattern)
            

        # Register attribute on the Token. We'll be overwriting this based on
        # the matches, so we're only setting a default value, not a getter.
        # If no default value is set, it defaults to None.
        Span.set_extension("index_term", default=False)
        

    def __call__(self, doc):
        """Apply the pipeline component on a Doc object and modify it if matches
        are found. Return the Doc, so it can be processed by the next component
        in the pipeline, if available.
        """
        matches = self.matcher(doc)
        spans = []  # keep the spans for later so we can merge them afterwards
        for _, start, end in matches:
            # Generate Span representing the entity 
            entity = Span(doc, start, end)
            entity._.index_term = self.entity_list.loc[entity.text].index_term
            
        return doc  # don't forget to return the Doc!


def write_index(nlp, texts, entry_lists, index_file):
    return 0
    df = build_dataframe(nlp, texts)
    df['index_term']=df['entity'].where(df.index_term == False)
    rng = 5
    mask = [n for n in nos if n > t-4 if n < t+4]
    [(df.start5 > entity.start - rng) & \
        (df.start < entity.start + rng) & \
        (df.page_no == entity.page_no)]  
    page_nos = df[df.entity == i.entity.text].page_no.to_list()
    def page_nos(nos): 
     ...:    curr = 0 
     ...:    for i in range(1,len(nos)-1): 
     ...:         if nos[i] == nos[i-1]+1: 
     ...:             continue 
     ...:         else:     
     ...:             yield '-'.join([str(nos[curr]), str(nos[i-1])]) 
     ...:             curr = i 

    if not entity.primary.isnull():
        page_nos = page_nos + \
        [' '.join((r.index_term, r.page_no) for r in df[mask])]
    return page_nos
    
    ranges=lambda l:map(lambda x:(x[0][1],x[-1][1]),map(lambda (x,y):list(y),itertools.groupby(enumerate(l),lambda (x,y):x-y)))
'''
