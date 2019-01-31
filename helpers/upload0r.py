#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Upload a file line by line using echo commands
# Usage: python3 upload0r.py [file]
# author: pschmied

import sys
import random
import string
import base64

filename = sys.argv[1]

# random tag
rnd = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

with open(filename) as f:
    lines = f.readlines()

for line in lines[:-1]:
    encoded = base64.b64encode(line.encode()).decode()
    print("echo '%s' | base64 -d >> /tmp/yolofile_%s && \\" % (encoded, rnd))

print("echo '%s' | base64 -d >> /tmp/yolofile_%s" %
      (base64.b64encode(lines[-1].encode()).decode(), rnd))
