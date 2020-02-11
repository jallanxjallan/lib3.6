#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
from pdf2image import convert_from_path
import pytesseract
import re
import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

sys.path.append('/home/jeremy/Library')
from document import PDFDocument


# In[3]:


nlp = spacy.load('en_core_web_sm', disable=['tagger', 'ner'])
matcher = Matcher(nlp.vocab)
pattern = [{"TEXT": {"REGEX": "\(cid\:\d+\)"}}]
matcher.add("CID", None, pattern)


# In[4]:


pdf_source = '2---7661EN6) Basics Int.pdf'


# In[5]:


images = convert_from_path(pdf_source)


# In[6]:


pdf_doc = PDFDocument(pdf_source)


# In[7]:


cid_pat = re.compile('(\(cid\:\d\))')


# In[13]:


pattern = [{"TEXT": {"REGEX": "\(cid\:\d+\)*?"}}]
matcher.add("CID", None, pattern)
ocr = [nlp(pytesseract.image_to_string(i)) for i in images]



# In[17]:


for tb in pdf_doc.parse_document():
    
    text = tb.text_box.get_text()
    if not re.search('cid\:\d', text, re.M):
        continue
    doc = nlp(text.replace("\n", " "))
    ocr_page = ocr[tb.page_no]
    
    
    for _, start, end in matcher(doc):
        phmatcher = PhraseMatcher(nlp.vocab)
        head_match = nlp(str(doc[start-4:start-1]))
        tail_match = nlp(str(doc[end+1:end+4]))
        
        phmatcher.add('HEAD', None, head_match)
        phmatcher.add('TAIL', None, tail_match)
        for match_id, start, end in phmatcher(ocr_page):
            print(nlp.vocab.strings[match_id], ocr_page[start:end])
            print('=======')
       
       
    


# In[ ]:


for l in ocred.split('\n'): print(l)


# In[ ]:


import sys
sys.path.append('/home/jeremy/Library')
from document import PDFDocument


# In[ ]:


pdf_source = '/home/jeremy/Desktop/vansit/source/2---7661EN6) Basics Int.pdf'


# In[ ]:


doc = PDFDocument(pdf_source)


# In[ ]:


[t for p in doc.pages for t in p.text_boxes()]


# In[ ]:


from pytesseract import Output


# In[ ]:


Images


# In[ ]:


monday = pytesseract.image_to_data(images[0],lang='eng', output_type='data.frame')


# In[ ]:


pytesseract.get_tesseract_version()


# In[ ]:




