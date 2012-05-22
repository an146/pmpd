#!/usr/bin/env python3
import os
import json
import urllib.request

os.chdir('waves/')
f = open('difm', 'w')
s = urllib.request.urlopen('http://listen.di.fm/public3/').read().decode('utf-8')
for x in json.loads(s):
    print(x['key'] + ': ' + x['playlist'], file=f)
