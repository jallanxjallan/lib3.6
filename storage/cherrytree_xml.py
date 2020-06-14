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
from lxml.etree import XPathEvalError
import base64
import urllib

@attr.s
class Codebox():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.content = self.element.text
        self.language = self.element.attrib['language']

@attr.s
class Anchor():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.name = self.element.attrib['anchor']

@attr.s
class Link():
    element = attr.ib()
    def __attrs_post_init__(self):
        self.text = self.element.text
        args = self.element.attrib['link'].split()
        self.type = args[0]
        if self.type == 'file':
            self.href = base64.b64decode(args[1]).decode()
        else:
            self.href = args[1]

class Node():
    def __init__(self, node):
        self.element = node
        self.name = node.attrib['name']

    @property
    def texts(self):
        # [l for n in itree.elements('Narrative') for t in n.texts for l in t.split("\n") if len(l.strip()) > 0]
        return (e.text for e in self.element.iter('rich_text') if e.text)

    @property
    def links(self):
        return (Link(l) for l in self.element.findall('rich_text[@link]'))

    @property
    def codeboxes(self):
        return (Codebox(c) for c in self.element.xpath('codebox'))

    @property
    def anchors(self):
        return (Anchor(a) for a in self.element.xpath('encoded_png'))

    def insert_link(self, href, text, target=None):
        element = etree.Element('rich_text')
        href = base64.b64encode(href.encode("utf-8")).decode()
        element.attrib['link'] = f'file {href}'
        element.text = text
        if target:
            target.element.addnext(element)
        else:
            self.element.insert(0, element)
        return Link(element)

    def insert_codebox(self, content, language='yaml', target=None):
        atts = dict(
            language=language,
            char_offset="10",
            frame_height="200",
            frame_width="700",
            highlight_brackets="True",
            show_line_numbers="False",
            syntax_highlighting='yaml',
        )
        element = etree.Element('codebox', atts)
        element.text = content
        if target:
            target.element.addnext(element)
        else:
            self.element.append(element)
        return Codebox(element)


    def insert_text(self, content, target=None):
        element = etree.Element('rich_text')
        element.text = content
        if target:
            target.element.addnext(element)
        else:
            self.element.append(element)
        return content

    def insert_anchor(self, name, target=None):
        element = etree.Element('encoded_png',
                                char_offset="0",
                                anchor=name)
        if target:
            target.element.addnext(element)
        else:
            self.element.append(element)
        return Anchor(element)


class CherryTree():
    def __init__(self, filepath):
        if type(filepath) is str:
            filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError
        self.tree = etree.parse(str(filepath))
        self.root = self.tree.getroot()
        self.filepath = filepath

    # @property
    # def unique_id(self):
    #     if not hasattr(self, '_unique_id'):
    #         self._unique_id = max([int(n.unique_id) for n in self.nodes() if hasattr(n, 'unique_id')])
    #     self._unique_id += 1
    #     return str(self._unique_id)

    def save(self, *arg):
        if arg:
            filepath = Path(arg[0])
        else:
            filepath = self.filepath
        with filepath.open('wb') as outfile:
            outfile.write(etree.tostring(self.tree))

    def nodes(self, base=None):
        if base:
            if type(base) is str:
                try:
                    base_node = self.find_node_by_name(base).node
                except:
                    return False
            else:
                base_node = base
        else:
            base_node = self.tree.getroot()

        for element in base_node.iter():
            if element.tag == 'node':
                yield Node(node=element)

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

    def find_node_by_pattern(self, pat):
        try:
            m = self.tree.xpath(f"//a[re:match(text(), {pat})]",
                namespaces={"re": "http://exslt.org/regular-expressions"})
        except XPathEvalError:
            print(f'bad xpath {pat}')
            return False
        return m

    def find_node_by_text(self, text):
        try:
            m = self.tree.xpath(f'//*[contains(., "{text}")]')
        except XPathEvalError:
            print(f'bad xpath {text}')
            return False
        if not m:
            return False
        return next((Node(n) for n in reversed(m) if n.tag == 'node'), None)

    def insert_node(self, name, target=None):
        unique_id = max([int(id.attrib['unique_id']) for id in self.tree.xpath('//node[@unique_id]')])
        timestamp = str(time.time())
        element = etree.Element('node',
                name=name,
                unique_id=str(unique_id + 1),
                custom_icon_id="0",
                foreground="",
                is_bold="False",
                prog_lang="custom-colors",
                readonly="False",
                ts_creation=timestamp,
                ts_lastsave=timestamp
            )
        if target:
            target.element.addnext(element)
        else:
            self.root.append(element)
        return Node(element)
