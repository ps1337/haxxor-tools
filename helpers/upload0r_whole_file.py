#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Upload a whole file using echo commands
# File can be a binary
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

with open(filename, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()
print("echo '%s' | base64 -d >> /tmp/yolofile_%s && \\" % (encoded, rnd))
print("chmod +x /tmp/yolofile_%s" % (rnd))
