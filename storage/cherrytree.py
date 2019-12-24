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

list_flags = dict(
    bulleted="•",
    numbered="[0-9]",
    checked="☑",
    unchecked="☐"
)

list_pats = {k:re.compile(f'{v}') for k,v in list_flags.items()}


from peewee import *

database = SqliteDatabase(None, **{})

class UnknownField(object):
    def __init__(self, *_, **__): pass
    
@attr.s
class Link():
    link = attr.ib()
    def __attrs_post_init__(self):
        self.text = self.link.text
        args = self.link.attrib['link'].split()
        if args[0]  == 'file':
            self.path = Path(base64.b64decode(args[1]).decode())
        elif args[0] == 'node':
            self.node = Node.get(Node.node == args[1])
        else:
            self.url = args[1]
        
            

@attr.s
class RichText():
    xml = attr.ib()
    def __attrs_post_init__(self):
        self.tree = etree.fromstring(self.xml)
        self.text = ' '.join([t.text for t in self.tree.iter('rich_text') if t.text])
        self.lines = self.text.split('\n')

    def list_items(self, ltype):
        lpat = list_pats[ltype] 
        for line in [l for l in self.lines if lpat.match(l)]:
            yield line
            
    def links(self, ltype):
        for link in [l for l in self.tree.findall('rich_text[@link]') if ltype in l.attrib['link']]:
           yield Link(link)
        
class RichTextField(Field):
    field_type = 'TEXT'
    
    def db_value(self, value):
        return str(value) # convert object into string.

    def python_value(self, xml):
        return RichText(xml) # convert to lxml object
    
class BaseModel(Model):
    class Meta:
        database = database

class Bookmark(BaseModel):
    node = IntegerField(column_name='node_id', null=True, unique=True)
    sequence = IntegerField(null=True)

    class Meta:
        table_name = 'bookmark'
        primary_key = False

class Children(BaseModel):
    father = IntegerField(column_name='father_id', null=True)
    node = IntegerField(column_name='node_id', null=True, unique=True)
    sequence = IntegerField(null=True)

    class Meta:
        table_name = 'children'
        primary_key = False

class Codebox(BaseModel):
    do_highl_bra = IntegerField(null=True)
    do_show_linenum = IntegerField(null=True)
    height = IntegerField(null=True)
    is_width_pix = IntegerField(null=True)
    justification = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    syntax = TextField(null=True)
    txt = RichTextField(null=True)
    width = IntegerField(null=True)

    class Meta:
        table_name = 'codebox'
        primary_key = False

class Grid(BaseModel):
    col_max = IntegerField(null=True)
    col_min = IntegerField(null=True)
    justification = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    txt = TextField(null=True)

    class Meta:
        table_name = 'grid'
        primary_key = False

class Image(BaseModel):
    anchor = TextField(null=True)
    filename = TextField(null=True)
    justification = TextField(null=True)
    link = TextField(null=True)
    node = IntegerField(column_name='node_id', null=True)
    offset = IntegerField(null=True)
    png = BlobField(null=True)
    time = IntegerField(null=True)

    class Meta:
        table_name = 'image'
        primary_key = False

class Node(BaseModel):
    has_codebox = IntegerField(null=True)
    has_image = IntegerField(null=True)
    has_table = IntegerField(null=True)
    is_richtxt = IntegerField(null=True, default=True)
    is_ro = IntegerField(null=True, default=False)
    level = IntegerField(null=True)
    name = TextField()
    node = IntegerField(column_name='node_id', null=True, unique=True)
    syntax = TextField(null=True)
    tags = TextField(null=True)
    txt = RichTextField(null=True)
    
    @property
    def parent(self):
        father = Children.get(Children.node == self.node)
        try:
            return Node.get(Node.node == father.father)
        except:
            return None

    @property
    def ancestors(self):
        def walk_up(parent):
            while True:
                try:
                    parent = parent.parent
                except:
                    break
                yield parent
        return list(reversed([p for p in walk_up(self) if p]))

    @property
    def children(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == self.node).order_by(Children.sequence):
            yield node
    
    @property
    def siblings(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == self.parent.node).order_by(Children.sequence):
            if not node.node== self.node:
                yield node
    
    @property
    def sequence(self):
        return Children.get(Children.node == self.node).sequence
    
    class Meta:
        table_name = 'node'
        primary_key = False

class KeyValue(BaseModel):
    key = TextField()
    value = TextField()
    node = ForeignKeyField(Node, field='node', column_name='node_id')
    
    class Meta:
        table_name = 'key_value'
        primary_key = False

class CherryTree():
    def __init__(self, filepath, root_node=0):
        fp = Path(filepath)
        if not fp.exists():
            raise FileNotFoundError
        self.db = database
        self.db.init(filepath)
        self.db.connect()
        
            
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.db.close()

    def find_node_by_id(self, no):
        try:
            return Node.get(Node.node == no)
        except Exception as e:
            print(e)
            return False

    
    def find_node_by_name(self, namepath):
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
                
    def all_nodes(self):
        for node in Node.select():
                yield node
    
    def select_top_nodes(self):
        for node in Node.select().join(Children, on=(Node.node == Children.node)).where(Children.father == 0):
            yield node
