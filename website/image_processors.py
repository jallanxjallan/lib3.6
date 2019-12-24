#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>


import sys
import os

from PIL import Image

size = (128, 128) # put that in config


def process_image(infile, outfile):
    try:
        im = Image.open(infile)
    except FileNotFoundError:
        raise
    try:
        im.thumbnail(size)
        im.save(outfile, "JPEG")
    except IOError:
        raise
    return outfile
    

