#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import uuid
from pathlib import Path

def identifier(length=8):
    return uuid.uuid4().hex[:8]

def class_name(obj):
    return obj.__class__.__name__

def filtered_tuple(tpl, **data):
    d = {snake_case(k1):v1 for k1,v1 in data.items()}
    return tpl(**{k:v for k,v in d.items() if k in tpl._fields})

def snake_case(text):
    return text.lower().replace(' ', '_')

def title_case(text):
    return text.replace('_', ' ').title()


class lazyloader(object):
    """
    Lazy-loading read-only property descriptor.
    Value is computed and stored in owner class object's dictionary on first
    access. Subsequent calls use value in owner class object's dictionary
    directly.
    """

    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, obj_class):
        if obj is None:
            return obj
        obj.__dict__[self.__name__] = self._func(obj)
        return obj.__dict__[self.__name__]

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
