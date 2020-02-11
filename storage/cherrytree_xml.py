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

logger = logging.getLogger(__name__)

token_specification = [
    ('bulleted', r"•"),
    ('numbered', r"[0-9]"),
    ('checked', r"☑"),
    ('unchecked', r"☐")
    ]
tok_regex = '|'.join('^(?P<%s>%s.*.?)$' % pair for pair in token_specification)
    

@attr.s
class ListItem():
    text = attr.ib()
    
@attr.s
class TextItem():
    text = attr.ib()
    kind = attr.ib(default='text')
    
@attr.s
class Anchor():
    anchor = attr.ib()
    node = attr.ib()
    
    def __attrs_post_init__(self):
        self.name = self.anchor.values().pop(0)

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
    
    
    @property
    def text_items(self):
        texts = []
        for elem in self.node.iter('rich_text'):
            if elem.get('link'):
                yield Link(elem)
            else:
                for line in elem.text.split('\n'):
                    if re.match(tok_regex, line):
                        yield ListItem(line)
                    else:
                        texts.append(line)
        if len(texts) > 0:
            yield TextItem('\n'.join(texts))
        
    
    @property
    def descendants(self):
        yield self
        for child in [d for d in self.node.iterdescendants() if d.get('name')]:
            yield Node(child)
            
    @property
    def ancestors(self):
        for parent in [p for p in self.node.iterancestors() if p.get('name')]:
            yield Node(parent)
            
    @property
    def parent(self):
        try:
            return Node(self.node.get_parent())
        except Exception as e:
            print(e)
            return False
            
    @property
    def text(self):
        return ' '.join([t.text for t in self.node.iter('rich_text') if t.text])
        
        
    @property
    def links(self):
        for link in [l for l in self.node.findall('rich_text[@link]')]:
           yield Link(link)
           
    @property
    def anchors(self):
        for anchor in self.node.findall('encoded_png[@anchor]'):
           yield Anchor(anchor, self)
        
           
class CherryTree():
    def __init__(self, filepath):
        if type(filepath) is str: 
            filepath = Path(filepath) 
        if not filepath.exists():
            raise FileNotFoundError
        self.tree = etree.parse(str(filepath))
        
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
        
'''
        
        def match_paths(node):
            ancestors = [a.name for a in node.ancestors]
            score = sum([fuzz.ratio(ns, ans) for ns, ans in zip(names, ancestors[-name_length:])]) / name_length
            if score > 90:
                return (score, node)
            else:
                return None
            
        names = namepath.split('/')
        target = names.pop(-1)
        name_length = len(names)
        if name_length > 0:
            qr = Node.select().where(Node.name.startswith(target[0]))
            path_matches = filter(None, [match_paths(n) for n in qr])
            return max(path_matches, key=itemgetter(0))[1]
        else:
            return Node.get(Node.name == target)
'''
                
   
