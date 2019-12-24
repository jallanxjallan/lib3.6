#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
from bs4 import BeautifulSoup
from lxml import etree
from lxml.html import builder as E
import pypandoc
import plac

CONTENT_PAT = './/Content'

def main(icml_dir, target_file):
    for filepath in [os.path.join(source_dir, f) for f in os.listdir(source_dir)]:
        try:
            tree = etree.parse(filename)
        except XMLSyntaxError:
            print(f'parsing error on {filename}')
            continue
        
        contents = ' '.join([e.text for e in tree.findall(CONTENT_PAT)])
    classes = ['Body---Box-Text-', 'Paragraph-Style-2', 'Basic-Paragraph', 'Bodi-Text']
    
    soup = BeautifulSoup(Path(html_source).read_text(), 'lxml')
    for div in soup.find_all('div'):
        try:
            layout_id = div['id'] if div['id'].startswith('_idContainer') else None
        except KeyError:
            continue
        if not layout_id: 
            continue
            
        try:
            content = [p.get_text() for p in div.find_all('p') if p['class'][0] in classes]
        except KeyError:
            continue
        if len(content) == 0:
            continue
                    
        filepath = Path(text_dir, layout_id[1:]).with_suffix('.md')
        pypandoc.convert_text('\n'.join(content), format='html', to='markdown', outputfile=str(filepath))

if __name__ == '__main__':
    main()
    
'''

#~ make_pdf_data(pdf_source)
    #~ df = pd.read_pickle(pdf_data) 

def make_pdf_data(pdf_source):
    df = pd.DataFrame([(p.page_no, b.position, b.text) \
            for p in parse_pdf_document(pdf_source) \
            for b in p.text_boxes()], columns=['page_no', 'position', 'text'])
    df.to_pickle(pdf_data)
try: 
            row = df[df.text.str.contains(para.string)]
        except TypeError:
            continue
        print (row.page_no, para.string)
'''
