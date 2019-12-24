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

sys.path.append('/home/jeremy/library')

from utility.helpers import snake_case

label_pat = re.compile('([a-z]|[A-Z].*)(\:|\;)(.*)')


#todo: convert supplied labels to words and match text_words[0:first len(label_words] 

def extract_labelled_text(text, labels, score_cutoff=90, best_match=True):
    """Parse text lines that start with strings fuzzy matching supplied labels""" 
    labelled_text = {}
    unlabelled_text = []
    for line in text.split('\n'):
        # skip blank lines
        if len(line.strip()) < 1:
            continue
            
        words = TextBlob(line).words
        
        possible_labels = snake_case('_'.join(words[0:2]))
    
        
        matches = [(l, fuzz.ratio(l, possible_labels)) for l in labels]
       
        
        if not matches:
            unlabelled_text.append(line)
            continue
   
        best_match = max(matches, key=itemgetter(1))
        
        if best_match[0] == 0 and best_match[1] > score_cutoff:
            labelled_text[best_match[0]] = ' '.join(words[2:])
        else:
            unlabelled_text.append(line)
    return labelled_text, '\n'.join(unlabelled_text)
