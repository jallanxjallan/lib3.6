#!/home/jeremy/Python3.6Env/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys 
import os

from imapclient import IMAPClient

from .emessage import EMessage 

tag_map = dict(recipient='TO', sender='FROM', subject='SUBJECT', seen='SEEN')

class EReader():
    def __init__(self, host, user, pwd, port=None):
        if port:
            self.reader = IMAPClient(host, port)
        else:
            self.reader = IMAPClient(host)
        self.reader.login(user, pwd)
        
    def upload(self, folder, message):
        self.reader.append(folder, str(message))
    
    def select_folder(self, folder):
        self.reader.select_folder(str(folder))
        
    def get_messages(self, folder, **kwargs):
        self.reader.select_folder(str(folder))
        messages = self.reader.search('SEEN')
        for uid, message_data in self.reader.fetch(messages, 'RFC822').items():
            yield uid, EMessage().load_message(message_data[b'RFC822'])
            
    def search(self, **kwargs):
        args = []
        for k,v in kwargs.items():
            args.append(tag_map[k])
            args.append(v)
        return self.reader.search(args)
        
    def logout(self):
        self.reader.logout()
        
    def __getattr__(self, attr):
        if hasattr(self.reader, attr):
            return getattr(self.reader, attr)
            
            


