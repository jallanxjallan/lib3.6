#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  module.py
#  
#  Copyright 2019 Jeremy Allan <jeremy@jeremyallan.com>

import sys
import os

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

textfile = '/home/jeremy/Projects/language_bureau/marketing_emails/test_mail.txt'

# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = 'ted@thelanguagebureau.com'
msg['To'] = 'jeremy@jeremyallan.com'

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
print(s.send_message(msg))
s.quit()
