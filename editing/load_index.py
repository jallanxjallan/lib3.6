import sys
import pandas as pd
from pathlib import Path
sys.path.append('/home/jeremy/Library')
from storage.cherrytree_xml import CherryTree
from document.md_document import MDDocument



def load_data(obj, columns):
    for column in columns:
        if hasattr(obj, column):
            yield getattr(node, column)


def load_from_stream(columns):
    files = load_files([MDDocument.read_file(f)) for f in sys.stdin.read()])
    data = [()]
    return pd.DataFrame(data, columns=columns)

def load_from_index(dindex, base_node=None, columns=None):
    try:
        idx = CherryTree(dindex)
    except FileNotFoundError:
        return pd.DataFrame([f'{dindex} not found'])


return pd.DataFrame(data, columns=columns).rename(columns={'name':'name_'})
    nodes = load_nodes([(n, MDDocument.read_file(n.filepath)) for in idx.nodes(base_node]])
