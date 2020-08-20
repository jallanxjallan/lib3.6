import sys
import pandas as pd
from pathlib import Path
from collections import defaultdict

sys.path.append('/home/jeremy/Library')
from storage.cherrytree_xml import CherryTree
from document.md_document import MDDocument


def load_record_data(obj, columns):
    item = {}
    for column in columns:
        if hasattr(obj, column):
            item[column] = getattr(obj, column)
    return item

def load_from_filepaths(filepaths, columns):
    data = []
    for filepath in filepaths:
        doc = MDDocument.read_file(filepath)
        doc_item = load_record_data(doc, columns)
        data.append(doc_item)
    return pd.DataFrame(data)

def load_from_index(dindex, columns, base_node=None):
    try:
        idx = CherryTree(dindex)
    except FileNotFoundError:
        return pd.DataFrame([f'{dindex} not found'])

    data = []
    for node in idx.nodes(base_node):
        node_item = load_record_data(node, columns)
        if node.filepath:
            doc = MDDocument.read_file(node.filepath)
            doc_item = load_record_data(doc, columns)
            data.append({**node_item, **doc_item})
        else:
            data.append(node_item)

    return pd.DataFrame(data)
