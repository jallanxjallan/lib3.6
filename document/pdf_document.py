#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_pdf_content.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@Jeremyallan.com>



import os
import re
import attr


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument as PDFDoc
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator

from pdf2image import convert_from_path
import pytesseract

import spacy



@attr.s
class TextItem():
    text_box = attr.ib()
    layout = attr.ib()
    page_no = attr.ib()
    document = attr.ib()
    
    @property
    def doc(self):
        if not hasattr(self, "_doc"):
            setattr(self, "_doc", self.document.nlp(self.text_box.get_text()))
        return self._doc

class PDFDocument():
    def __init__(self, pdf_source):
        self.pdf_source = pdf_source
        
        
    @property
    def images(self):
        if not hasattr(self, "_images"):
            setattr(self, "_images", convert_from_path(self.pdf_source))
        return self._images
    
    @property
    def nlp(self):
        if not hasattr(self, "_nlp"):
            setattr(self, "_nlp", spacy.load('en_core_web_sm'))
        return self._nlp

    def parse_document(self):
        with open(self.pdf_source, "rb") as infile:
            # Create parser object to parse the pdf content
            parser = PDFParser(infile)
            
            # Store the parsed content in PDFDocument object
            document = PDFDoc(parser)

            # Check if document is extractable, if not abort
            if not document.is_extractable:
                raise PDFTextExtractionNotAllowed
            
            # Create PDFResourceManager object that stores shared resources such as fonts or images
            rsrcmgr = PDFResourceManager()

            # set parameters for analysis
            laparams = LAParams()
            

            # Create a PDFDevice object which translates interpreted information into desired format
            # Device needs to be connected to resource manager to store shared resources
            device = PDFDevice(rsrcmgr)
            # Extract the decive to page aggregator to get LT object elements
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create interpreter object to process page content from PDFDocument
            # Interpreter needs to be connected to resource manager for shared resources and device 
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # Ok now that we have everything to process a pdf document, lets process it page by page
            
            
            for no, page in enumerate(PDFPage.create_pages(document)):
                # As the interpreter processes the page stored in PDFDocument object
                interpreter.process_page(page)
                layout = device.get_result()
                
                for text_box in [b for b in layout if isinstance(b, LTTextBox)]:
                    yield TextItem(text_box, layout, no, self)


''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
 Fortunately, though, each object also provides a bbox (bounding box) attribute, which is a four-part tuple of the object's page position: (x0,
y0, x1, y1)
x0: the distance from the left of the page to the left edge of the box.
 y0: the distance from the bottom of the page to the lower edge of the box.
 x1: the distance from the left of the page to the right edge of the box.
 y1: the distance from the bottom of the page to the upper edge of the box.

Remember in PDF the page origin is the *bottom left corner*.
So the bottom left is (0,0) and the top right corner is
somewhere like (612,792) in the case of A4 paper.

def __attrs_post_init__(self):
        (minx, miny, maxx, maxy) = self.tbox.bbox
        self.top_left = (minx, maxy)
        self.top_right = (maxx, maxy)
        self.bottom_left = (minx, miny)
        self.bottom_right = (maxx, miny) 

def component_name(layout, bounding_box):
    import json
    (minx, miny, maxx, maxy) = bb
    return json.dumps(dict(
        minx=minx,
        miny=miny,
        maxx=maxx,
        maxy=maxy,
        x0=ly.x0,
        x1=ly.x1,
        y0=ly.y0,
        y1=ly.y1,
        height=ly.height,
        width=ly.width
        )
    )
    
    #~ if (maxx - minx) > ly.width/2 and (maxy - miny) > ly.height/2:
        #~ return "main_text"
    #~ elif ly.x1 - maxy < 10:
        #~ return "header"
    #~ elif miny - ly.x0  < 10:
        #~ return "footer"
    #~ else:
        #~ return "unknown"
        

['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_objs', 
'add', 'analyze', 'bbox', 'extend', 'get_text', 'get_writing_mode', 'hdistance', 'height', 'hoverlap', 'index', 'is_empty', 'is_hoverlap', 'is_voverlap', 'set_bbox', 'vdistance', 'voverlap', 'width', 'x0', 'x1', 'y0', 'y1']


'''
