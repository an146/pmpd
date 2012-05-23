#!/usr/bin/env python3
import os
import json
import urllib.request

s = urllib.request.urlopen('http://listen.di.fm/public3/').read().decode('utf-8')
for x in json.loads(s):
    f = open('waves/difm/' + x['key'], 'w')
    print('# ' + x['description'], file=f)
    print(x['playlist'], file=f)
