#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import select
Base = declarative_base()

sql_filepath = 'sqlite:////home/jeremy/Projects/language_bureau/student/data/students.db'



class Alchemy():
    def __init__(self, db_filepath):
        self.engine = create_engine(sql_filepath)
        self.metadata = MetaData(self.engine)
        #~ metadata.create_all()
        self.metadata.reflect(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)()
        self.query = self.session.query
    
    def close(self):
        self.session.close()
    
    def get_table(self, name):
        return self.metadata.tables[name]
    
    def run_query(self, query):
        res = self.session.query(query)
        for _row in res:
            yield _row


