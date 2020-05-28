#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import fire
from pathlib import Path
import spacy

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.read_document import read_document

nlp = spacy.load('en_core_web_sm')

def extract_named_entities(text_index, target_node=None):
    ct = CherryTree(text_index)

    sp = Path('/home/jeremy/Projects/arie_smit')

    documents = [(read_document(sp.joinpath(n.text_filepath)), n) for n in ct.nodes(target_node) if n.text_filepath]

    docs = nlp.pipe([(d[0].content, d[1]) for d in documents], as_tuples=True)

    for (node, ent) in [(d[1], e) for d in docs for e in d[0].ents]:
        yield (node, ent)
