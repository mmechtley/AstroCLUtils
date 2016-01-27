#!/usr/bin/env python
"""
astrodrizzle keeps certain fits header keywords from every one of the original
files used to create the final, drizzled file. For large or deep survey fields,
this may be header keywords from hundreds of individual images, and can
significantly contribute to the file size of small stamp images extracted from
the full, combined image. This utility removes these DXXX keywords from an
image's fits header.

Usage:
strip_drizzle_keys.py fits1.fits [...] fitsn.fits
"""
import sys
from astropy.io import fits
import re

# Single-drizzle keywords begin with D followed by 3 digits
_key_pat = re.compile('^D\d{3}')

def strip_drizzle_keys(filename):
    with fits.open(filename, mode='update') as fd:
        for key, value in fd[0].header.items():
            if _key_pat.match(key):
                del fd[0].header[key]
        fd.flush()
    print('Removed single-driz keywords from {}'.format(filename))
    return

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        strip_drizzle_keys(filename)