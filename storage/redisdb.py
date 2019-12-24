#!/home/jeremy/PythonEnv/bin/python
# -*- coding: utf-8 -*-
#
#  script.py
# 

"""
Redis key generator
generates key with standardized prefix, namespace, types and identifiers
generates key parts from lookup mapping  
to ensure keyname consistency and eliminate typing errors 
"""

import redis
import yaml
import json
import re

KEYSEP = ':'
NAME_SEP = '.'

class RedisKey():
    """creates object with defined key and redis connection access"""
    def __init__(self, r, name, *args, **kwargs):
        self.r = r
        self._expire = kwargs.get('expire') or r.keydefs.expire 
        
        if name.startswith(self.r.keydefs.namespace + ':'):
            self.key = name
        else:
            self.key = self.make_key(name, *args, **kwargs)
        
    def persist(self):
        self.r.conn.persist(self.key)
        self._expire = None
        return True
    
    def make_key(self, name, *args, **kwargs):
        key_base = KEYSEP.join((self.r.keydefs.namespace, *getattr(self.r.keydefs, name)))
        if '{uid}' in key_base and not 'uid' in kwargs:
            kwargs['uid'] = make_uid()
        key = key_base.format(**kwargs)
        if 'expire' in kwargs:
            self._expire = kwargs['expire']
        return key
        
    def __str__(self):
        return self.key
        
    def convert_to_key(self, arg):
        if isinstance(arg, RedisKey):
            return str(arg)
        else:
            return arg
    
    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            if not hasattr(self.r.conn, attr):
                raise AttributeError(attr)
            rs = getattr(self.r.conn, attr)(self.key, *[self.convert_to_key(a) for a in args], **kwargs)
            if rs == True:
                if self.r.conn.ttl(self.key) == -1 and not self._expire is None:
                    self.r.conn.expire(self.key, self._expire)
                return self
            else:
                return rs
        return wrapper
                
class RedisDB():
    """creates connection to redis a factory for producing RedisKey objects"""
    def __init__(self, config=None, host='127.0.0.1', port='6379'):
        self.conn=redis.StrictRedis(host, port, decode_responses=True)
        if config:
            self.keydefs = config.redis

    def make_key(self, key):
        return RedisKey(self, key)
    
    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            if hasattr(self.conn, attr):
                return getattr(self.conn, attr)(*args, **kwargs)
            elif attr in self.keydefs._fields:
                return RedisKey(self, attr, *args, **kwargs) 
            else:
                raise AttributeError(attr)
        return wrapper
        
    
