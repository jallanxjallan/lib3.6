#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
#
#  Config.py
#
#  Copyright 2016 Jeremy Allan
#
#

import sys
import os
import namedtupled
import yaml

#yaml loader unsafe. Need to write my own nested tupler
yaml.warnings({'YAMLLoadWarning': False})


def load_config(filepath=None):
    config_path = filepath or os.getcwd()
    if not config_path.endswith('yaml'):
        config_path = os.path.join(config_path, 'config.yaml')
    try:
        return namedtupled.yaml(path=config_path)
    except FileNotFoundError:
        print(config_path, ' not found')
        return False

def nested_tuple(mapping, name):
    def tupperware(mapping):
        if isinstance(mapping, collections.Mapping):
            for key, value in mapping.items():
                mapping[key] = tupperware(value)
            return nested_tuple(mapping)
        return mapping
    
    this_namedtuple_maker = collections.namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)

class ConfigBase():

    def load_nt(self, filename):
        return namedtupled.yaml(path=os.path.join(self.basedir, filename+'.yaml'))

    def load_dict(self, filename):
        mapping = self.load_nt(filename)
        return namedtupled.reduce(mapping)
        

