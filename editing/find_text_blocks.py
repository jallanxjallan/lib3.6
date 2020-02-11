#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import spacy
from pathlib import Path
import itertools
nlp = spacy.load('en_core_web_sm', disable=['ner', 'pos', 'parser'])
from matplotlib.pyplot import plot


# In[18]:


def word_filter(w):
    if w.is_stop:
        return False
    if w.is_punct:
        return False
    return True


# In[30]:





synopsis = nlp(Path('/home/jeremy/Test/test_data/synopsis.txt').read_text())
scene = nlp(Path('/home/jeremy/Test/test_data/scene.txt').read_text())

scene_array = [(t.text, t.i) for t in scene if word_filter(t)]
synopsis_array = [(t.text, t.i) for t in synopsis if word_filter(t)]
it = pd.DataFrame([(p[0][1], p[1][1],                 fuzz.ratio(p[0][0], p[1][0]))                 for p in itertools.product(scene_array, synopsis_array)],                  columns=['source_idx', 'target_idx', 'similarity'])
it['bin'] = 0
sims = it[it.similarity > 95]

bin_size = len(synopsis_array) / len(scene_array)

groups = sims.groupby(['bin', pd.cut(sims.target_idx, bins=bin_size)])
groups.size()
    
    


# In[32]:


synopsis[739:831]


# In[8]:


it.describe()


# In[ ]:




