#!/usr/bin/python
"""
Opens the specified files in ds9, with regions of the same file name, e.g.:
ds9_with_regions.py ibnb*.fits
"""

import subprocess
import glob
import sys
import os

# takes in a glob with optional fits extension, returns tuple list of file,ext
def globfits(fglob):
    if fglob[-1] == "]":
        fglob, ext = fglob[:-1].rsplit("[")
        if ext.isdigit():
            ext = int(ext)
        return [(file, ext) for file in glob.glob(fglob)]
    else:
        return [(fglob, None) for file in glob.glob(fglob)]

if len(sys.argv) < 2:
    print(__doc__)
    exit(1)
	
files = sum([globfits(arg) for arg in sys.argv[1:]], []) # sum flattens

call_sig = ['ds9']
for file, ext in files:
    if ext is not None:
        call_sig += ['{}[{}]'.format(file, ext)]
    else:
        call_sig += ['{}'.format(file, ext)]
    call_sig += ['-regions', '{}.reg '.format(os.path.splitext(file))[0]]

subprocess.call(call_sig)