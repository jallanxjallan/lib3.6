#!/home/jeremy/ProjectPython/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
#

import sys
import redis
import re
from textblob import TextBlob

sys.path.append('/home/jeremy/pi/library/')

from gdrive import GDrive

r = redis.StrictRedis(decode_responses = True)

rkey = 'newsletter:items'
url = 'http://balidiscovery.com/news/raising-a-glass-to-a-better-tomorrow'



def main():

    content = r.hget(rkey, url).replace('|', ' ')
    blob = TextBlob(content)
    sentences = [s for s in blob.sentences if len(s) > 50]


    for sentence in :
        print(sentence)
        print('-')
        #~ for sentence in blob.sentences:
            #~ if sentence.startswith('*') or sentences[-1].endswith('*'):
                #~ sentences[-1] += ' ' + str(sentence)
            #~ else:
                #~ sentences.append(str(sentence))

    #~ for sentence in sentences:
        #~ if len(sentence) > 50:
            #~ print(sentence)




if __name__ == '__main__':
    main()
