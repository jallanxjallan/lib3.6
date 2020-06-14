#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  update_document_index.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
import datetime
import attr
import fire
import inflect

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.md_document import read_file

@attr.s
class Document():
    index = attr.ib()
    document = attr.ib()
    filepath = attr.ib(converter=lambda x: x.href)

    def __attrs_post_init__(self):
        self.name = self.index.name
        self.notes = '\n'.join((t for t in self.index.texts))

    def __getattr__(self, attr):
        if not self.document.metadata:
            return None
        return self.document.metadata.get(attr, None)


class DocumentIndex():
    def __init__(self, index_file='document_index.ctd'):
        try:
            self.ct = CherryTree(index_file)
        except Exception as e:
            print(e)
            raise

    def documents(self, base=None):
        for node in self.ct.nodes(base):
            filelink = next((l for l in node.links if l.type == 'file'), None)
            if not filelink:
                continue
            document = self.load_document(filelink.href)
            if not document:
                continue
            yield Document(node, document, filelink)

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


    def add_document(self, document, filepath):
        if self.ct.find_node_by_text(document.identifier):
            print(filepath, 'already indexed')
            return True
        node = self.ct.insert_node(document.title)
        anchor = node.insert_anchor(name=document.identifier)
        link = node.insert_link(href=filepath, text="File", target=anchor)
        new_line = node.insert_text('\n')
        return True

    def load_document(self, filepath):
        try:
            document = read_file(filepath)
        except FileNotFoundError:
            print(filepath, 'not found')
            return False
        return document
