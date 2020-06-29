#!/home/jeremy/Python3.6Env/bin/python
# * coding: utf8 *
#
#  update_document_index.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
from uuid import uuid4
import attr
import fire
sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.md_document import read_file

def load_document(filepath):
    try:
        document = read_file(filepath)
    except FileNotFoundError:
        print(filepath, 'not found')
        return False
    if not document.identifier:
        print(filepath, 'has no identifier')
        return False
    if not document.title:
        print(filepath, 'has no title')
        return False
    return document

@attr.s
class IndexEntry():
    node = attr.ib()
    document = attr.ib(default=None)

    def __str__(self):
        return str(self.document)

    def __attrs_post_init__(self):
        self.name = self.node.name
        self.identifier = next((a.name for a in self.node.anchors), None)
        self.filelink = next((l.href for l in self.node.links if l.type == 'file'), None)
        self.notes = '|'.join((t for t in self.node.texts if len(t.strip()) > 0))

    def __getattr__(self, attr):
        try:
            return getattr(self.node, attr)
        except AttributeError:
            pass
        if not self.filelink:
            return None
        if self.document is None:
            self.document = load_document(self.filelink)
        try:
            return getattr(self.document, attr)
        except AttributeError:
            pass
        try:
            return self.document.metadata.get(attr, None)
        except AttributeError:
            pass
        return None

class DocumentIndex():
    def __init__(self, index_file, base_node=None):
        self.index_file = index_file
        self.base_node = base_node
        try:
            self.ct = CherryTree(index_file)
        except Exception as e:
            print(e)
            raise

    def list_entries(self):
        for node in self.ct.nodes():
            yield IndexEntry(node)

    def save_index(self):
        return self.ct.save()

    def find_entry_by_name(self, name):
        rs = self.ct.find_node_by_name(name)
        if rs:
            return IndexEntry(rs)

    def find_entry_by_identifier(self, identifier):
        rs = self.ct.find_node_by_attribute('anchor', identifier)
        if rs:
            return IndexEntry(rs)

    def insert_document_link(self, node, document):
        node.insert_anchor(document.identifier)
        node.insert_link(document.filepath, text='Content')
        return True



    # def store_document_data(self, node, data):
    #     if not type(data) is str:
    #         content = dump_yaml(data)
    #     else:
    #         content = data
    #
    #     codebox = next((c for c in node.codeboxes), None)
    #     if codebox:
    #         codebox.content = content
    #     else:
    #         node.insert_codebox(content=dump_yaml(content), language='yaml')
