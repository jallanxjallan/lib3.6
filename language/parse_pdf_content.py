#!/home/jeremy/ProjectPython/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
# 

import sys 
import os
import pandas as pd
from textblob import TextBlob
from nltk import RegexpParser

sys.path.append('/home/jeremy/library/document')
from pdf_document import extract_pages

NP = 'NP: {<NN|VB|NN.*>+}'
chunker = RegexpParser(NP)

def make_dataframe(pdf_source, output_filepath=None):
    def box_row(p, t):
        data = t._asdict()
        data['page_no'] = p.page_no
        return data
 
    boxes = [box_row(p,t) for p in extract_pages(pdf_source) for t in p.text_boxes()]
    df = pd.DataFrame(boxes)
    if output_filepath:
        df.to_pickle(output_filepath)
    else:
        return df
    return True
    
def output_text(df):
    p_20 = df[(df['page_no'] == '20') & (df['minx'] < 1000)].sort_values('maxy', ascending=False)
    for row in p_20.itertuples(): 
        blob = TextBlob(row.text) 
        for sent in blob.sentences: 
            print(chunker.parse(sent.tags))
            
     


    

    
