#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from fuzzywuzzy import process
from collections import defaultdict

def filtered_tuple(tpl, **data):
    d = {snake_case(k1):v1 for k1,v1 in data.items()}
    return tpl(**{k:v for k,v in d.items() if k in tpl._fields}) 
    
def snake_case(text):
    return text.lower().replace(' ', '_')
    
def title_case(text):
    return text.replace('_', ' ').title()
    
#~ def normalize_dict_keys(data, key_list):
    #~ def normalize_key(key, key_list):
        #~ choice, score = process.extractOne(key, key_list)
        #~ if score > 70:
            #~ return snake_case(choice)
        #~ else:
            #~ return key
            
    #~ cleaned = defaultdict(dict)
    #~ for key, value in data.items():
        #~ if type(value) is dict:
            #~ for k,v in value.items():
                #~ cleaned[key][normalize_key(key, key_list)] = v
        #~ else:
            #~ cleaned[normalize_key(key, key_list)] = value
    
    #~ for key in key_list:
        #~ try:
            #~ cleaned[key]
        #~ except KeyError:
            
    
    #~ return cleaned
