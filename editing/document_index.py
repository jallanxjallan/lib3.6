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
import datetime
from uuid import uuid4
import attr
import fire
import inflect
import pypandoc
sys.path.append('/home/jeremy/Library')

from storage.cherrytree_xml import CherryTree
from document.md_document import read_file

@attr.s
class Document():
    index = attr.ib()
    document = attr.ib()
    filepath = attr.ib()

class DocumentIndex():
    def __init__(self, index_file=None, base_node=None):
        print('index', index_file)
        self.index_file = index_file
        self.base_node = base_node
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

    def save_index(self):
        return self.ct.save()

    def add_document(self, fp):

        if not fp.exists():
            return False
        elif not fp.is_file():
            return False
        elif not fp.suffix == '.md':
            return False

        document = read_file(str(fp))
        if not document:
            return False
        print(document.title, document.identifier)

        if self.ct.find_node_by_text(document.identifier):
            print(filepath, 'already indexed')
            return True
        base_node = self.ct.find_node_by_name(self.base_node) \
            or self.ct.insert_node(self.base_node)
        title = document.title or re.sub('\|\_', ' ', fp.stem).title()
        node = self.ct.insert_node(title, parent=base_node)
        anchor = node.insert_anchor(name=document.identifier)
        link = node.insert_link(href=str(fp), text="File", sibling=anchor)
        new_line = node.insert_text(f'\n{"~" * 30}\n')
        return fp

    def add_from_filelist(self, filelist):
        fp = Path(filelist)
        added = []
        for filepath in [Path(f) for f in fp.read_text().split("\n")]:
            added.append(self.add_document(filepath))
        self.save_index(added)


    def add_from_filename(self, filepath):
        rs = self.add_document(filepath)
        if rs:
            self.save_index([rs])
        return True

    def add_from_stream(self):
        added = []
        for filepath in sys.stdin.readlines():
            fp = Path(filepath.strip())
            added.append(self.add_document(fp))
        self.save_index(added)
        return True

    def add_file_link(self, filepath):
        document = read_file(filepath)
        node = self.ct.find_node_by_text(document.identifier)
        if node:
            return f'{filepath} already linked to {node.name}'
        node = self.ct.find_node_by_name(document.title)

        if not node:
            return f'Cannot find node matching {document.title}'

        anchor = node.insert_anchor(document.identifier)
        node.insert_link(href=document.filepath, text="Content")

        return f'Link to {filepath} added to {node.name}'


    def export_to_file(self, node_name, target_dir):
        target_path = Path(target_dir)
        node = self.ct.find_node_by_name(node_name)

        if not node:
            return f'Cannot find node {node_name}'

        identifier = uuid4().hex[:8]
        outputfile = target_path.joinpath(node_name.replace(' ', '_').lower()).with_suffix('.md')
        if outputfile.exists():
            print(f'{str(outputfile)} already exists')
        outputfile=str(outputfile)
        content = "\n".join([t for t in node.texts if len(t) > 0])
        try:
            pypandoc.convert_text(content,
                              'markdown',
                              format='markdown',
                              outputfile=outputfile,
                              extra_args=[
                                  f'metadata=identifier:{identifier}',
                                  f'metadata=title:{node.name}',
                                  'defaults=create_document'
                              ])
        except Exception as e:
            return e
        [e.getparent().remove(e) for e in node.element.iterchildren('rich_text')]
        anchor = node.insert_anchor(identifier)
        node.insert_link(href=outputfile, text="Content")
        self.ct.save()
        return f'Notes from {node.name} written to {outputfile}'
