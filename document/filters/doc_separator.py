#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

"""
Pandoc filter using panflute
"""

import panflute as pf

def prepare(doc):
    doc.doc_separator = doc.get_metadata('doc_separator')
    
def action(elem, doc):
    return elem
        
def finalize(doc):
    separator = []
    
    for tag in doc.doc_separator.split():
        try:
            separator.append(doc.get_metadata(tag))
        except KeyError:
            separator.append(tag)
    doc.content.insert(0, pf.Header(pf.Str(' '.join(separator), level=1))
    
    del doc.doc_separator


def main(doc=None):
    return pf.run_filter(action,
                         prepare=prepare,
                         finalize=finalize,
                         doc=doc) 


if __name__ == '__main__':
    main()
