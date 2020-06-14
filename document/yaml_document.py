#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import attr

from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

yaml = YAML()
yaml.explicit_start = True
yaml.explicit_end = True
yaml.default_flow_style = False

def dump_yaml(data):
    stream = StringIO()
    yaml.dump(data, stream)
    stream.seek(0)
    return stream.read()

def load_yaml(data):
    return yaml.load(data)

@attr.s
class YAMLDocument():
    data = attr.ib(converter=lambda x: yaml.load(x) if type(x) is str else x)

    def __attrs_post_init__(self):
        for k,v in self.data.items():
            setattr(self, k, v)

    @property
    def data_dict(self):
        return self.data
