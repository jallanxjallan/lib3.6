#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cherrytree.py
#  

import re

from lxml import etree
from collections import namedtuple
import base64

import logging
logger = logging.getLogger(__name__)

UNCHECKEDBOX = "☐"
CHECKEDBOX = "☑"

Link = namedtuple('Link', ('label, type, url'))
NodeRow = namedtuple('NodeRow', ('level name node_id tags txt'))

ChildRow = namedtuple('ChildRow', ('father node sequence'))


from sqlite_orm.database import Database
from sqlite_orm.field import IntegerField, BooleanField, TextField
from sqlite_orm.table import BaseTable


class Children(BaseTable):
    __table_name__ = 'children'
    father_id = IntegerField()
    node_id = IntegerField()
    sequence = IntegerField()


class Node(BaseTable):
    __table_name__ = 'node'
    level = IntegerField()
    name = TextField()
    node_id = IntegerField()
    tags = TextField()
    txt = TextField()


class CherryTree():
    def __init__(self, filepath):
        self.db = Database(filepath)

    def close_database(self):
        self.db.close()

    
    def nodes(self):
        for node in self.db.query(Node).select().execute():
            yield NodeRow(*node)
            
    def children(self):
        for child in self.db.query(Children).select().execute():
            yield child
        

            
   

