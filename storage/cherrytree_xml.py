#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cherrytree.py
#

import sys
import os
import re
from pathlib import Path
from operator import itemgetter
import logging
import attr
from lxml import etree
import base64
from fuzzywuzzy import fuzz
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


@attr.s
class Link():
    link = attr.ib()
    text = attr.ib(default=None)
    filepath = attr.ib(default=None)
    url = attr.ib(default=None)
    node_id = attr.ib(default=None)
    node_anchor = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.text = self.link.text
        args = self.link.attrib['link'].split()
        if args[0] == 'file':
            self.filepath = Path(base64.b64decode(args[1]).decode())
        elif args[0] == 'web':
            self.url = args[1]
        elif args[0] == 'node':
            self.node_id = args[1]
            if len(args) > 2:
                self.node_anchor = args[2]


@attr.s
class Node():
    node = attr.ib()

    def __attrs_post_init__(self):
        for k,v in self.node.attrib.items():
            setattr(self, k, v)

    def read_codebox(self):
        codebox = self.node.child('codebox')
        yaml = YAML()
        return yaml.loads(codebox.text)

    def write_codebox(self, code):
        atts = dict(
            char_offset="0",
            frame_height="200",
            frame_width="700",
            highlight_brackets="True",
            show_line_numbers="False",
            syntax_highlighting='yaml',
            width_in_pixels="True"
        )
        e = etree.Element('codebox', atts)
        e.text = code
        self.node.append(e)


    @property
    def links(self):
        for link in [l for l in self.node.findall('rich_text[@link]')]:
           yield Link(link)

    def make_file_link(self, filepath, text):
        link = etree.Element('rich_text', link=base64.b64encode(filepath)
        link.text=text
        self.node.append(e)
        
class CherryTree():
    def __init__(self, filepath):
        if type(filepath) is str:
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError
        self.tree = etree.parse(str(filepath))
        self.filepath = filepath

    @property
    def unique_id(self):
        if not hasattr(self, '_unique_id'):
            self._unique_id = max([int(n.unique_id) for n in self.nodes()])
        self._unique_id += 1
        return str(self._unique_id)

    def save(self, *arg):
        if arg:
            filepath = Path(arg[0])
        else:
            filepath = self.filepath
        with filepath.open('wb') as outfile:
            outfile.write(etree.tostring(self.tree))

    @property
    def root(self):
        return self.tree.getroot()

    def nodes(self):
        root = self.tree.getroot()
        for element in root.iter():
            if element.tag == 'node':
                yield Node(element)

    def find_node_by_id(self, id):
        try:
            return Node(self.tree.xpath(f'//node[@unique_id={id}]')[0])
        except Exception as e:
            print(e)
            return False

    def find_node_by_name(self, name):
        try:
            return Node(self.tree.xpath(f'//node[@name="{name}"]')[0])
        except Exception as e:
            print(e)
            return False
