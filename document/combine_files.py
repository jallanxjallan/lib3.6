-*- coding: utf-8 -*-
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



def combine_files(args_filepath, *input_files, **output_args):

    try:
        args = load_config(args_filepath)
    except Exception as e:
        print(e)
        exit()

    with TemporaryDirectory() as tmpdir:
        temppath = Path(tmpdir)
        pandoc_config_filepath = tfile('.yaml')
        with pcf.open('w') as outfile:
            yaml.dump(pandoc_config, pcf)


        pandoc_commands = []
        

        for input_file in input_files:
            output_file = temppath.joinpath(uuid4().hex).with_suffix('.md')
            output_args['input-files'].append(output_file)
            pandoc_commands.append(f'pandoc -d {str(pcf)} -o {output_file} {input_file}')

        output_args_file = temppath.joinpath(uuid4().hex).with_suffix('.yaml')

        with output_args_file.open('w') as outfile:
            yaml.dump(output_args, output_args_file)

        pandoc_commands.append(f'pandoc -d {str(output_args_file)}')

        bash_filepath = tmpdir.joinpath('batch_file.sh')
        bash_filepath.write_text('\n'.join(pandoc_commands))

        subprocess.run(['bash', str(bash_filepath)])
