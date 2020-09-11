#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rediskey.py
#

import sys
from string import Template
import attr

sys.path.append('/home/jeremy/Library')
from utility.helpers import make_identifier

@attr.s
class RedisKey():
    namespace = attr.ib()
    component = attr.ib()
    id = attr.ib(default="$id")

    def __attrs_post_init__(self):
        self.key = Template(':'.join((self.namespace, self.component, self.id)))


    def k(self, id=None):
        return self.key.substitute(id=id if id else make_identifier())
