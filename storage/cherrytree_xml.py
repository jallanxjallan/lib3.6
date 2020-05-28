#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cherrytree.py
#

import sys
import os
import re
from pathlib import Path
import logging
import attr
import time
from lxml import etree
import base64


@attr.s
class Codebox():
    def make_box():
        atts = dict(
            char_offset="0",
            frame_height="200",
            frame_width="700",
            highlight_brackets="True",
            show_line_numbers="False",
            syntax_highlighting='yaml',
            width_in_pixels="True"
        )
        return etree.Element('codebox', atts)

    element = attr.ib(default=attr.Factory(make_box))
    content = attr.ib(default=attr.Factory(lambda self: self.element.text, takes_self=True))

    def __attrs_post_init__(self):
        if self.element.text == None:
            self.element.text = self.content

    def update_content(self, content):
        self.element.text = content


@attr.s
class Link():
    def make_link():
        return etree.Element('rich_text')
    def format_href(href):
        if href.startswith('file'):
            return f'file {base64.b64encode(href.encode("utf-8")).decode()}'
        else:
            return f'web {href}'

    def extract_href(self):
        args = self.element.attrib['link'].split()
        self.type = args[0]
        if args[0] == 'file':
            href = base64.b64decode(args[1]).decode()
        elif args[0] == 'web':
            href = args[1]
        elif args[0] == 'node':
            href = args[1]
        return href
    element = attr.ib(default=attr.Factory(make_link))
    href = attr.ib(default=attr.Factory(extract_href), converter=format_href)
    text = attr.ib(default=attr.Factory(lambda self: self.element.text, takes_self=True))

    def __attrs_post_init__(self):
        if not hasattr(self.element, 'link'):
            self.element.attrib['link'] = self.href
            self. element.text = self.text

@attr.s
class Node():
    def make_node():
        timestamp = str(time.time())
        node = etree.Element('node',
            custom_icon_id="0",
            foreground="",
            is_bold="False",
            prog_lang="custom-colors",
            readonly="False",
            ts_creation=timestamp,
            ts_lastsave=timestamp
        )
        return node

    node = attr.ib(default=attr.Factory(make_node))
    name = attr.ib(default=attr.Factory(lambda self: self.node.attrib['name'], takes_self=True))

    def __attrs_post_init__(self):
        for k,v in self.node.attrib.items():
            setattr(self, k, v)

    @property
    def links(self):
        for link in [l for l in self.node.findall('rich_text[@link]')]:
           yield Link(link)

    @property
    def codeboxes(self):
        for box in self.node.xpath('codebox'):
            yield Codebox(box)

    def insert_element(self, obj, position=-1):
        if hasattr(obj, 'element'):
            element = obj.element
        else:
            element = obj

        self.node.insert(0,element)

class CherryTree():
    def __init__(self, filepath):
        if type(filepath) is str:
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError
        self.tree = etree.parse(str(filepath))
        self.root = self.tree.getroot()
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

    def nodes(self, start=None):
        if start:
            base_node = start.node
        else:
            base_node = self.tree.getroot()

        for element in base_node.iter():
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

    def insert_node(self, node, position=-1):
        if hasattr(node, 'node'):
            node = node.node
        node.attrib['unique_id'] = self.unique_id
        self.root.insert(position, node)
