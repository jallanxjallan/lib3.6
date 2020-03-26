#!/home/jeremy/PythonEnv3.6/bin/python
#
#  module.py
#
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

from tempfile import TemporaryDirectory
import logging
from pathlib import Path
import subprocess

def run_bash_script(cmds):
    with TemporaryDirectory() as tmpdir:
        temppath = Path(tmpdir)
        bash_filepath = temppath.joinpath('bash_script.sh')
        bash_filepath.write_text('\n'.join(cmds))
        try:
            rs = subprocess.run(['bash', str(bash_filepath)], stdout=subprocess.PIPE)
        except Excpetion as e:
            print(e)
            return False
        return rs.stdout
