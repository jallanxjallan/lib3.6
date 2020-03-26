#!/home/jeremy/PythonEnv3.6/bin/python
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
from collections import defaultdict
from itertools import tee
from tempfile import TemporaryDirectory
import logging
from pathlib import Path
import yaml
import subprocess
import pypandoc

sys.path.append('/home/jeremy/Library/')
from utility.config import load_config
from utility.helpers import identifier

with Path('/home/jeremy/Library/document/pandoc_config_fields.yaml').open() as infile:
    PANDOC_CONFIG_FIELDS = yaml.load(infile)

def batch_convert(args):
    def write_config_file(d):
        data = {k:v for k,v in d.items() if k in PANDOC_CONFIG_FIELDS}
        filepath = temppath.joinpath(identifier()).with_suffix('.yaml')
        with filepath.open('w') as outfile:
            yaml.dump(data, outfile)
        return filepath

    with TemporaryDirectory() as tmpdir:
        temppath = Path(tmpdir)
        interfiles = []
        pandoc_commands = []
        for item in args:
            if 'input-files' in item:
                infiles = []
                for file in item['input-files']:
                    filepath = Path(file) if type(file) is str else file
                    if filepath.stem in interfiles:
                        infiles.append(temppath.joinpath(file))
                    else:
                        infiles.append(filepath)

                item['input-files'] = [str(f) for f in infiles]

            if 'input-file' in item:
                file = item['input-file']
                filepath = Path(file) if type(file) is str else file
                if filepath.stem in interfiles:
                    filepath = temppath.joinpath(filepath)
                item['input-file'] = str(filepath)

            if 'inter-file' in item:
                file = item['inter-file']
                filepath = Path(file) if type(file) is str else file
                item['output-file'] = str(temppath.joinpath(file))
                interfiles.append(file.stem)
            else:
                item['output-file'] = str(item['output-file'])

            pandoc_commands.append(f'pandoc -d {write_config_file(item)}')


        bash_filepath = temppath.joinpath('batch_file.sh')
        bash_filepath.write_text('\n'.join(pandoc_commands))
        rs = subprocess.run(['bash', str(bash_filepath)], stdout=subprocess.PIPE)
        return rs.stdout
