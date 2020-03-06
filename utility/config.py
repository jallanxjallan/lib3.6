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
from pathlib import Path
import yaml

#yaml loader unsafe. Need to write my own nested tupler
# yaml.warnings({'YAMLLoadWarning': False})


def load_config(arg):
    if type(arg) is dict:
        return arg
    elif type(arg) is str and arg.endswith('.yaml'):
        try:
            with Path(arg).open() as infile:
                return yaml.load(infile)
        except FileNotFoundError as e:
            print(f'Could not load {arg}')
            raise e
    elif type(arg) is str:
        return yaml.load(arg)
    else:
        print('Not a config file')
        raise TypeError

'''
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
'''
