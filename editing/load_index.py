import sys
import pandas as pd
from pathlib import Path
sys.path.append('/home/jeremy/Library')
from storage.cherrytree_xml import CherryTree
from document.md_document import read_file

def load_index(dindex, base_node=None, columns=None):
    try:
        idx = CherryTree(dindex)
    except FileNotFoundError:
        return pd.DataFrame([f'{dindex} not found'])

    data = []
    for node in idx.nodes(base_node):
        try:
            doc = read_file(next((l.href for l in node.links if l.type == 'file'), None))
        except:
            doc = None

        cols = []
        for column in columns:
            if hasattr(node, column):
                cols.append(getattr(node, column))
            elif doc and hasattr(doc, column):
                cols.append(getattr(doc, column))
            else:
                cols.append(None)
        data.append(cols)

    return pd.DataFrame(data, columns=columns).rename(columns={'name':'name_'})
