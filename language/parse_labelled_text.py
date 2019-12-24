#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  match_text.py

import sys
import re
from operator import itemgetter
from fuzzywuzzy import process, fuzz
from collections import namedtuple
from textblob import TextBlob

sys.path.append('/home/jeremy/Library')

from utility.helpers import snake_case

label_pat = re.compile('([a-z]|[A-Z].*)(\:|\;)(.*)')

LabeledText = namedtuple('LabeledText', ('label, text'))

def parse_labelled_text(text, labels, score_cutoff=90, best_match=True):
    for line in text.split('\n'):
        if len(line.strip()) < 1:
            continue
            
        blob = TextBlob(line)
        
        matches = [(l, i, fuzz.ratio(l, w.lower())) for i, w in enumerate(blob.words) for l in labels]
        
        if not matches:
            yield LabeledText('text', line)
            continue
            
        best_match = max(matches, key=itemgetter(2))
        
        if best_match[1] == 0 and best_match[2] > score_cutoff:
            pat = '{}\:\s'.format(blob.words[best_match[1]])
            
            yield LabeledText(best_match[0], re.sub(pat, '', line))
        else:
            yield LabeledText('text', line)
