#!/home/jeremy/PythonEnv3.6/bin/python
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from collections import defaultdict
from itertools import tee
from uuid import uuid4
from tempfile import TemporaryDirectory
import logging
from pathlib import Path
import yaml
import subprocess
import pypandoc

sys.path.append('/home/jeremy/Library/')
from utility.config import load_config

with Path('/home/jeremy/Library/document/pandoc_config_fields.yaml').open() as infile:
    PANDOC_CONFIG_FIELDS = yaml.load(infile)

def combine_files(args_filepath, *input_files, **output_args):
    def write_config_file(d):
        data = {k:v for k,v in d.items() if k in PANDOC_CONFIG_FIELDS}
        filepath = temppath.joinpath(uuid4().hex).with_suffix('.yaml')
        with filepath.open('w') as outfile:
            yaml.dump(data, outfile)
        return filepath

    try:
        input_args = load_config(args_filepath)
    except Exception as e:
        print(e)
        exit()

    with TemporaryDirectory() as tmpdir:
        temppath = Path(tmpdir)
        input_args_file = write_config_file(input_args)

        pandoc_commands = []
        if type(output_args) is None:
            output_args = {}
        output_args['input-files'] = []

        for input_file in input_files:

            output_file = str(temppath.joinpath(uuid4().hex).with_suffix('.md'))
            output_args['input-files'].append(output_file)
            pandoc_commands.append(f'pandoc -d {input_args_file} -o {output_file} {str(input_file)}')

        pandoc_commands.append(f'pandoc -d {write_config_file(output_args)}')


        bash_filepath = temppath.joinpath('batch_file.sh')
        bash_filepath.write_text('\n'.join(pandoc_commands))

        rs = subprocess.run(['bash', str(bash_filepath)], stdout=subprocess.PIPE)
        if len(rs.stdout) == 0:
            return output_args['output-file']
        return rs.stdout
