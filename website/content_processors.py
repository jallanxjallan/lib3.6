#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

def content_image(href):
    

    
def get_linked_content(node, c, label):
    link = next((l for l in node.links if l.type == 'file' if l.label == label), None)
    if not link:
        return None
    filepath = os.path.join(c.base_path, link.url)
    try:
        text = read_document(filepath)
    except FileNotFoundError:
        return None

def process_links(soup):
    for link in soup.findall('a'):
        

def process_images(soup):
    for image in soup.findall('img'):
        image['href']= content_image(image['href'])
        image_url = url_for('static', filename=os.path.basename(x))
    if not os.path.exists(image_url):
        image_url = resize_for_web(href, image_url)
    return 

    image = image_url
    
    if image:
        


def content(node, c, label):
    text = get_linked_content(node, c, label)
    if not text:
        return None
    
    soup = BeautifulSoup(text, 'lxml')
    process_images(soup)
    
    return str(soup)

    
