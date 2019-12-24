#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

import smtplib
from smtplib import SMTPRecipientsRefused, SMTPConnectError, SMTPServerDisconnected


class EServer():
    def __init__(self, host, port, user, pwd, ssl=True, debug=False):
        if debug:
            self.server = smtplib.SMTP('localhost', 1025)
        else:
            try:
                self.server = smtplib.SMTP_SSL(host, port) if ssl else  smtplib.SMTP(host, port)
            except SMTPConnectError as e:
                raise e
            self.server.login(user, pwd)
    
    def send_message(self, message):
        try:
            self.server.send_message(message)
        except SMTPServerDisconnected:
            raise
        except SMTPRecipientsRefused as e:
            return str(e)
        return 'today'
            
    def quit(self):
        self.server.quit()
