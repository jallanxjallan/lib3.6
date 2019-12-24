#!/home/jeremy/ProjectPython/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#

import sys
import os
import re
import logging

import requests
from bs4 import BeautifulSoup


def get_page(url):
    try:
        rs = requests.get(url)
    except ConnectionError:
        logging.warn('Unable to open {}'.format(url))
        return None
    return BeautifulSoup(rs.text, 'lxml')
    
    
def get_text_content(soup):
    body = soup.find('body')

    for em in body.findAll('em'):
        parent = em.parent
        text = next(em.stripped_strings, None)
        em.replace_with('*' + text + '* ')
        
    #~ for tag in body.findAll(['style', 'script']):
        #~ tag.dispose()

    
    return [dict(name=t.parent.name, text=t.get_text(separator="|", strip=True)) for t in body.findAll('p')] or None
