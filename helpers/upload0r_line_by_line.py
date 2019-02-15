#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Upload a file in small chunks using echo commands
# File can be a binary
# Usage: python3 upload0r.py [file]
# author: pschmied

import sys
import random
import string
import base64
import re

CHUNKSIZE = 40

filename = sys.argv[1]

# random tag
rnd = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

with open(filename, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# Split in `CHUNKSIZE` chunks
chunks = re.findall('.' * CHUNKSIZE, encoded)

for chunk in chunks:
    print("echo -ne '%s' >> /tmp/.yolofile_%s && \\" % (chunk, rnd))

print("cat /tmp/.yolofile_%s | base64 -d > /tmp/yolofile_%s && \\" % (rnd, rnd))
print("rm /tmp/.yolofile_%s && chmod +x /tmp/yolofile_%s" % (rnd, rnd))
