#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os
from pathlib import Path
import plac
from lxml import etree
from lxml.etree import XMLSyntaxError
import spacy
import textacy
import textacy.preprocessing as tp
from peewee import *

database = SqliteDatabase(None, **{})

class BaseModel(Model):
    class Meta:
        database = database
        
class Story(BaseModel):
    filepath = TextField()
    updated = DateTimeField(default=datetime.datetime.now())
    dispatched = DateTimeField(default=datetime.datetime.now())
    
class Paragraph(BaseModel):
    text = TextField()
    story = ForeignKeyField(Story)
    
class Entity(BaseModel):
    text = TextField()
    
class ParagraphEntity(BaseModel):
    paragraph = ForeignKeyField(Paragraph)
    entity = ForeignKeyField(Entity)
    
    

#~ def clean_text(text):
    #~ doc = nlp(text)
    #~ for sent in doc.sents:
        #~ yield ' '.join([w.text for w in textacy.extract.words(sent, filter_stops=True, filter_punct=True)])
    
     
def parse_icml_content(filepath):
    tree = etree.parse(filepath)
    contents = []
    for e in tree.getroot().iter('Content', 'Br'):
        if e.tag == "Content":
            contents.append(e.text)
        elif e.tag == 'Br':
            yield ' '.join(contents)
            contents = []
        else:
            pass
    if len(contents) > 0:
        return ' '.join(contents)
    else:
        return True
    
    
def main(icml_folder, icml_db):
    icml_source= Path(icml_folder)
    database.init(icml_db)
    nlp = spacy.load('en_core_web_sm')
    db = database.connect()
    if  len(db.get_tables() == 0:
        db.create_tables([Story, Paragraph, Entity, ParagraphEntity])
    
    for icml_file in icml_folder.iterdir():
        story, screated = Story.get_or_create(filepath=str(icml_file))
        
        for paragraph in parse_icml_content(filepath):
            doc = nlp(paragraph)
            para, pcreated = Paragraph.get_or_create(text=paragraph)
            for ent in doc.ents:
                entity, ecreated = Entity.get_or_create(text=ent.text)
                ParagraphEntity.get_or_create(paragraph=para, entity=ent)
    db.save()
    db.close()


if __name__ == '__main__':
    plac.call(main)
    
