#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os
#~ import base64

import pypandoc

import email
from email.utils import formataddr, parseaddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from email.policy import default
from email.message import EmailMessage

class EMessage():
    def __init__(self):
        self.content = []
        
        
    def create_message(self):
        self.msg = EmailMessage()
        return self
        
    def load_message(self, msg):
        p = email.parser.BytesFeedParser(policy=default)
        p.feed(msg)
        self.msg = p.close()
        return self
            
    @property
    def recipient(self):
        return parseaddr(self.msg['To']) 
    
    @recipient.setter
    def recipient(self, *args):
        self.msg['To'] = formataddr(*args)
        
    @property
    def sender(self):
        return parseaddr(self.msg['From']) 
    
    @sender.setter
    def sender(self, *args):
        self.msg['From'] = formataddr(*args)
        
    @property
    def subject(self):
        return self.msg['Subject']
    
    @subject.setter
    def subject(self, subject):
        self.msg['Subject'] = subject

    @property
    def main_content(self):
        content = None
        if self.msg.is_multipart():
            for part in self.msg.walk():
                if (part.get_content_type() == 'text/plain') and (part.get('Content-Disposition') is None):
                    content = part.get_payload()
        else:
            content = self.msg.get_payload(decode=True)
        return content #base64.b64decode(content)
        
    def get_content(self):
        #~ return extract_body(self.msg)[0]
        simplest = self.msg.get_body(preferencelist=('plain', 'html'))
        return simplest.get_content()
    
    def set_content(self, item):
        #~ simplest = self.msg.get_body(preferencelist=('plain', 'html'))
        return self.msg.set_content(item)
    
    def add_main_content(self, item):
        self.content.append(item)
        return True
    
    def attach_pdf(self, pdf_filepath, pdf_name='PDF'):
        attachment = open(pdf_filepath, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % pdf_name)
        self.msg.attach(part)
        return True
        
    def set_signature(self, signature_file):
        with open(signature_file, 'rb') as infile:
            self.signature = MIMEImage(infile.read())
            self.signature.add_header('Content-ID', '<{}>'.format('signature'))
            self.msg.attach(self.signature)
            return True
        
    def __str__(self):
        if hasattr(self, 'signature'):
             self.content.append('<p><img src="cid:signature" /></p>')
        if len(self.content) > 0: 
            self.msg.attach(MIMEText(pypandoc.convert_text('\n\n'.join(self.content), format='markdown', to='html'), 'html'))
        return str(self.msg)
        
def extract_body(msg, depth=0):
    """ Extract content body of an email messsage """
    body = []
    if msg.is_multipart():
        main_content = None
        # multi-part emails often have both
        # a text/plain and a text/html part.
        # Use the first `text/plain` part if there is one,
        # otherwise take the first `text/*` part.
        for part in msg.get_payload():
            is_txt = part.get_content_type() == 'text/plain'
            if not main_content or is_txt:
                main_content = extract_body(part)
            if is_txt:
                break
        if main_content:
            body.extend(main_content)
    elif msg.get_content_type().startswith("text/"):
        #~ # Get the messages
        #~ charset = msg.get_param('charset', 'utf-8').lower()
        #~ # update charset aliases
        #~ charset = email.charset.ALIASES.get(charset, charset)
        #~ msg.set_param('charset', charset)
        try:
            body.append(msg.get_content())
        except AssertionError as e:
            print('Parsing failed.    ')
            print(e)
        except LookupError:
            # set all unknown encoding to utf-8
            # then add a header to indicate this might be a spam
            msg.set_param('charset', 'utf-8')
            body.append('=== <UNKOWN ENCODING POSSIBLY SPAM> ===')
            body.append(msg.get_content())
    return body
