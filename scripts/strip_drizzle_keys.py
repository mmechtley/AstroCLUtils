#!/usr/bin/env python
import sys
import pyfits
import re

# Single-drizzle keywords begin with D followed by 3 digits
_key_pat = re.compile('^D\d{3}')

def strip_drizzle_keys(filename):
    with pyfits.open(filename, mode='update') as fd:
        for key, value in fd[0].header.items():
            if _key_pat.match(key):
                del fd[0].header[key]
        fd.flush()
    print 'Removed single-driz keywords from {}'.format(filename)
    return

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        strip_drizzle_keys(filename)