#!/usr/bin/env python
# coding: utf-8

import sys
from pathlib import Path
import attr
from redis import Redis
from subprocess import Popen, PIPE

sys.path.append('/home/jeremy/Library')

from document.yaml_document import load_yaml_from_file, dump_yaml_to_file
from utility.helpers import make_identifier

r = Redis()


@attr.s
class Defaults():
    input = attr.ib()
    output = attr.ib(attr.converters.optional(str))
    metadata = attr.ib(default=None)

    def __attrs_post_init__(self):
        if type(input) is list:
            self.inputs = [str(i) for i in self.input]
            self.input = None
        else:
            try:
                e = Path(self.input).exists()
            except:
                self.text = self.input
                self.input = None
            if e:
                self.input = str(self.input)
            else:
                self.text = self.input
                self.input = None


def make_default_file(defaults, tmpdir, rkeyindex):
    text = r.get(rkeyindex, 'text')
    if text:
        temp_filepath = tmpdir.joinpath(make_identifier()).with_suffix('md')
        temp_filepath.write_text(text)
        defaults['input-file'] = str(temp_filepath)
    else:
        input_key = r.hget(rkeyindex, 'input')
        input_type = r.type(input_key)

        if input_type is 'list':
            defaults['input-files'] = r.lrange(input_key)
        elif input_type is 'string':
            defaults['input-file'] = r.get(input_key)

    metadata = r.hgetall(r.hget(rkeyindex, 'metadata'))
    if metadata and defaults.exists('metadata'):
        defaults['metadata'].update(metadata)
    elif metadata:
        defaults['metadata'] = metadata

    output = r.get(r.hget(rkeyindex, 'output'))
    if output:
        defaults['output-file'] = output
    else:
        defaults['output-file'] = str(tmpdir.joinpath(make_identifier())).with_suffix('.md')

    defaults_filepath = str(tmpdir.joinpath(make_identifier())).with_suffix('.yaml')

    try:
        dump_yaml_to_file(defaults, defaults_filepath)
    except Exception as e:
        print(e)
        return None
    return defaults_filepath

def make_defaults(input=None, output=None, metadata=None):
    data = Defaults(input, output, metadata)
    key_id = make_identifier()
    master_key = f'pandoc::{key_id}:index'
    r.expire(master_key, 60)

    for key, att in attr.fields_dict(data).items():
        print(key)
        # rkey = f'pandoc::{key_id}:{key}'
        # r.expire(rkey, 60)
        # r.hset(master_key, key, rkey)
        # print(type(value))

        # if type(value) is str:
        #     r.set(rkey, str(input))
        # elif type(value) is list:
        #     r.lpush(rkey, *value)
        # elif type(value) is dict:
        #     r.hmset(rkey, value)

    return master_key

def run_pandoc(defaults, rkeys):
    if not type(defaults) is dict:
        defaults = load_yaml_from_file(defaults)

    with TemporaryDirectory() as tmpdir:
        default_files = [make_default_file(defaults.copy(), k) for k in rkeys]
        p = Popen(['pandoc_defaults.sh'], stdin=PIPE)
        rs = p.communicate(input=default_files, timeout=5)
        return rs
