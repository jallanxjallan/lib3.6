#!/home/jeremy/Scripts/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
import attr
from pathlib import Path
from ruamel.yaml import YAML

from .convert_document import file_to_text, text_to_text, text_to_file

MARKDOWN = 'markdown_mmd+yaml_metadata_block'
yaml=YAML(typ='safe') 

@attr.s
class Document():
    source = attr.ib()
    meta = attr.ib(factory=dict)
    
    def __attrs_post_init__(self):
        self.content = []
        source_file = Path(self.source)
        is_file = False
        try:
            is_file = source_file.exists()
        except OSError:
            pass
        
        if not is_file:
            self.content.append(text_to_text(self.source))
        else:
            if self.source.suffix in ('.md', '.txt'):
                text = self.source.read_text()
                try: 
                    meta, text = text.split('---')[1:]
                except IndexError:
                    meta = {}
                except ValueError:
                    meta = {}
                self.content.append(text)
                if len(meta) > 0:
                    self.meta = yaml.load(meta)
                else:
                    self.meta = {}
            else:
                self.content.append(file_to_text(self.source))
    
    def __str__(self):
        return '\n'.join(self.content)
        
    
    def write_document(self, filepath):
        if type(self.meta) is dict:
            extra_args = [f'--metadata={k}:{v}' for k,v in self.meta.items()]
        else:
            extra_args = []
        extra_args.append('--standalone')
        text_to_file(self.content, filepath, extra_args)

    
