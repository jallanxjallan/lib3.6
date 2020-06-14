#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import re
from pathlib import Path
import datetime
import attr
import inflect

sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree, Node, Link, Codebox
from document.yaml_document import YAMLDocument
from document.md_document import MDDocument


class DocumentIndex():
    def __init__(self, filename):
        try:
            self.ct = CherryTree(filename)
        except Exception as e:
            print(e)
            raise

    def add_file(self, fiiepath):
        try:
            document = Document(filepath)
        except FileNotFoundError:
            print(filepath, 'not found')
            return False
        node = self.ct.insert_node(document.title)
        node.insert_link(href=filepath, text=document.identifier))
        node.insert_codebox(content=document.meta.dump_yaml()), language='yaml')
        return node


# @property
#     def text_filepath(self):
#         filepath = None
#         codebox = self.codebox
#         if codebox and hasattr(codebox, 'filepath'):
#             filepath = codebox.filepath
#         else:
#             filepath = next((l.filepath for l in self.links if l.filepath), None)
#         return filepath
#
# def __attrs_post_init__(self):
#         yaml = YAML()
#         if len(self.data) > 0:
#             if type(self.data) is str:
#                 self.data = yaml.load(self.data)
#         else:
#             self.data = yaml.load(self.codebox.text)
#
#     def __str__(self):
#
#         stream = StringIO()
#         yaml.dump(self.codebox.text, stream)
#         stream.seek(0)
#         return stream.read()
#
#     def __getattr__(self, att):
#         return self.codebox.get(att, None)
# yaml=YAML()
# p = inflect.engine()
# # nlp = spacy.load('en_core_web_sm')
#

def add_file():



def update_document_index(index_file = 'document_index.ctd'):



    # ct = CherryTree(index_file)

    for text in sys.stdin.readlines():
        print(text)
        print('===========')
        # node = ct.find_node_by_text(document.identifier)
        # file_link = Link(None, document.filepath, 'Text')
        # metadata = CodeBox(None, document.metadata)
        # if node:
        #     node
        #
        #     node = Node(None, links=file_link, codeboxes=metadata)
        # try:
        #     node_data = YAMLDocument(next(c.content for c in node.codeboxes))
        # except Exception as e:
        #     print(e)
        #     continue












        # node = ct.create_node(title.title())
        # node.make_file_link(filepath, 'Text')
        # node.update_insert_codebox(metadata)
        # shutil.move(str(source_filepath), str(target_filepath))
        # ct.save()
